from __future__ import annotations
from pathlib import Path
from collections import Counter
import csv, json, html, hashlib
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs"
topics=list(csv.DictReader((ROOT/"sources/topics.tsv").open(encoding="utf-8"),delimiter="\t"))
pages=json.loads((ROOT/"sources/pages.json").read_text(encoding="utf-8"))
review=json.loads((ROOT/"sources/review.json").read_text(encoding="utf-8"))
manifest=json.loads((ROOT/"sources/manifest.json").read_text(encoding="utf-8"))
assert review["source_sha256"]==next(x["sha256"] for x in manifest if x["role"]=="primary"),"Source changed: review new pages before regenerating coverage"
assert review["text_pages"]==list(range(1,403)) and review["contact_page_count"]==402
def expand(text):
    out=[]
    for piece in filter(None,text.split(",")):
        if "-" in piece:
            a,b=map(int,piece.split("-"));out.extend(range(a,b+1))
        else:out.append(int(piece))
    return out

assigned={}
for topic in topics:
    path=DOCS/(topic["file"]+".md")
    assert path.exists(),path
    assert "{#"+topic["anchor"]+"}" in path.read_text(encoding="utf-8"),topic
    for p in expand(topic["pages"]):
        assert p not in assigned,(p,topic["id"],assigned.get(p))
        assigned[p]=topic

reviewed=review["detail_pages"]
structural=[]
for page in pages:
    p=page["page"]
    if p==264:page["kind"]="chapter-cover"
    page["visual_review"]="text+contact-sheet; detail" if p in reviewed else "text+contact-sheet"
    if p in assigned:
        t=assigned[p]
        page.update({"coverage":"mapped","knowledge_id":t["id"],"target":t["file"]+".md#"+t["anchor"],"depth":t["depth"]})
    else:
        assert page["kind"] in ["cover","chapter-cover","outline"],f"Unmapped content page {p}: {page['title']}"
        page.update({"coverage":"structural","knowledge_id":None,"target":"syllabus.md","depth":"结构与导航，不独立作为知识点"})
        structural.append(p)
(ROOT/"sources/pages.json").write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding="utf-8")

knowledge=["# 全课程知识点清单\n",
f"共 {len(topics)} 个稳定知识条目，其中 {sum(bool(t['pages']) for t in topics)} 个对应讲义内容，8 个为数学预备补充。条目按主题组织，页数和条目数都不等于教学质量。\n",
"重要性仅表示学习依赖：核心、支撑、拓展，不表示教师考试要求。讲授深度描述本笔记处理方式；原讲义中的计算图没有原始数据时，只解析方法和图意。\n"]
group=None
for t in topics:
    key=t["id"].split("-")[1]
    if key!=group:
        knowledge.extend([f"\n## {'数值附录' if key=='B' else '第 '+str(int(key))+' 部分'}\n",
        "| 编号 | 知识主题与正文 | 重要性 | 讲解深度 | 讲义物理页 |\n|---|---|---|---|---|"])
        group=key
    knowledge.append(f'| <span id="{t["id"].lower()}">{t["id"]}</span> | [{t["title"]}](./{t["file"]}.md#{t["anchor"]}) | {t["importance"]} | {t["depth"]} | {t["pages"] or "自学补充"} |')
(DOCS/"knowledge.md").write_text("\n".join(knowledge)+"\n",encoding="utf-8")

coverage=["# 讲义逐页覆盖索引\n",
f"402 页全部登记；{len(assigned)} 页内容映射到正文，{len(structural)} 页为封面、章节扉页或重复目录。这里的“覆盖”表示内容获得了明确处理，并不表示每张原始图的未提供数据已经复现。\n",
"全部页已作文字阅读与整页缩略图检查。公式异常、关键图示另作放大核对。表中页码为 bv_cvxslides.pdf 的物理页码，从 1 开始。\n",
"| 物理页 | 原页标题 | 处理与正文位置 |\n|---|---|---|"]
for page in pages:
    p=page["page"]
    title=html.escape(page["title"]).replace("|",r"\|").replace("\n"," ")
    if p in assigned:
        t=assigned[p]
        target=f'[{t["id"]} · {t["title"]}](./{t["file"]}.md#{t["anchor"]})；{t["depth"]}'
    else:target="结构页：用于章节与来源识别，不单独重写"
    coverage.append(f'| <span id="pdf-{p:03d}">{p}</span> | {title} | {target} |')
(DOCS/"coverage.md").write_text("\n".join(coverage)+"\n",encoding="utf-8")

manifest=json.loads((ROOT/"sources/manifest.json").read_text(encoding="utf-8"))
sourcefile=DOCS/"sources.md"
s=sourcefile.read_text(encoding="utf-8")
generated="\n## 文件指纹与范围 {#fingerprints}\n\n"
for x in manifest:
    generated+=f"### {x['file']}\n\n- 总页数：{x['pages']}。\n- 用途：{'主要内容覆盖' if x['role']=='primary' else '定义、推导与勘误参考，不宣称全书逐页覆盖'}。\n- SHA-256：\n\n~~~text\n{x['sha256']}\n~~~\n\n"
sourcefile.write_text(s.split("<!-- generated fingerprints -->")[0].rstrip()+"\n\n<!-- generated fingerprints -->\n"+generated,encoding="utf-8")
stats={"knowledge_points":len(topics),"lecture_points":sum(bool(t["pages"]) for t in topics),
       "supplement_points":sum(not bool(t["pages"]) for t in topics),
       "lecture_pages":402,"mapped_pages":len(assigned),"structural_pages":len(structural),
       "depth":dict(Counter(t["depth"] for t in topics))}
(ROOT/"sources/stats.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(stats,ensure_ascii=False))
