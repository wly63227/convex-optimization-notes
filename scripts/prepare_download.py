"""Generate the one-file Markdown edition from canonical docs; never hand edit it."""
from pathlib import Path
import os,re,shutil,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
order=["guide","00-foundations","01-modeling","02-sets","03-functions","04-problems","05-duality",
 "06-approximation","07-statistics","08-geometry","appendix-numerics","09-unconstrained",
 "10-equality","11-interior","12-practice","exercises","experiments","syllabus",
 "knowledge","coverage","sources","visualizations","maintenance","report"]
titles=[]
for name in order:
    s=(ROOT/"docs"/(name+".md")).read_text(encoding="utf-8")
    titles.append((name,re.search(r"^# (.+)",s)[1]))
chunks=["# 凸优化系统学习笔记\n\n依据本地 Boyd–Vandenberghe 讲义与教材整理。正文来源为 docs/；本文件自动生成，不直接维护。\n\n## 阅读目录\n"]
chunks += [f"- [{title}](#{name})" for name,title in titles]
for name,title in titles:
    s=(ROOT/"docs"/(name+".md")).read_text(encoding="utf-8")
    def heading(m):
        marks,label,anchor=m.group(1),m.group(2),m.group(3)
        aid=name+"-"+anchor if anchor else name if len(marks)==1 else ""
        return (f'<a id="{aid}"></a>\n' if aid else "")+"#"*min(len(marks)+1,6)+" "+label
    s=re.sub(r"^(#{1,5}) (.*?)(?: \{#([^}]+)\})?$",heading,s,flags=re.M)
    s=s.replace("<StepSizeLab />","（步长交互见网站；下方静态图与上文手算表提供相同的关键规律。）")
    def link(m):
        prefix,label,target=m.groups()
        path,sep,anchor=target.partition("#")
        stem=Path(path).stem
        if path.startswith("./assets/"):
            target="docs/assets/"+path.split("./assets/",1)[1]
        elif not path and sep:
            target="#"+name+"-"+anchor
        elif stem in order and path.endswith(".md"):
            target="#"+stem+("-"+anchor if sep else "")
        elif path.startswith("./") and path.endswith(".md"):
            target="docs/"+path[2:]+(sep+anchor if sep else "")
        return prefix+"["+label+"]("+target+")"
    s=re.sub(r"(!?)\[([^\]]*)\]\(([^)]+)\)",link,s)
    chunks.append("\n\n---\n\n"+s)
text="\n".join(chunks)
(ROOT/"凸优化系统学习笔记.md").write_text(text,encoding="utf-8")
download=ROOT/"docs/public/downloads";download.mkdir(parents=True,exist_ok=True)
(download/"凸优化系统学习笔记.md").write_text(text.replace("docs/assets/","assets/"),encoding="utf-8")
shutil.copytree(ROOT/"docs/assets",download/"assets",dirs_exist_ok=True)
with zipfile.ZipFile(download/"凸优化笔记与图表.zip","w",zipfile.ZIP_DEFLATED) as archive:
    archive.write(download/"凸优化系统学习笔记.md","凸优化系统学习笔记.md")
    for asset in sorted((download/"assets").glob("*.svg")):
        archive.write(asset,"assets/"+asset.name)
try:
    commit=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,capture_output=True).stdout.strip() or None
except OSError:commit=None
version={
    "edition":"1.0",
    "source":"canonical Markdown",
    "git_commit":commit,
    "published":os.environ.get("GITHUB_ACTIONS") == "true",
}
(ROOT/"docs/public/release.json").write_text(json.dumps(version,ensure_ascii=False,indent=2),encoding="utf-8")
print("Generated root Markdown, download copy, matching SVG assets, and release.json.")
