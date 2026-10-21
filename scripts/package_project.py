"""Bundle reviewed authoring sources, excluding PDFs, runtimes and build caches."""
from pathlib import Path
import zipfile,re,json
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/"凸优化系统学习笔记.md").read_text(encoding="utf-8")
anchors=set(re.findall(r'id="([^"]+)"',text))
for anchor in re.findall(r'\]\(#([^)]+)\)',text):
    assert anchor in anchors,("download anchor",anchor)
assert "<StepSizeLab" not in text
for image in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
    assert (ROOT/image).exists(),image
files=[]
for name in ["docs","scripts","examples","results","sources",".github"]:
    for file in (ROOT/name).rglob("*"):
        if not file.is_file():continue
        rel=file.relative_to(ROOT)
        if any(p in {"__pycache__","dist","cache","lecture-text"} for p in rel.parts):continue
        if rel.as_posix()=="sources/pages.json":continue
        files.append(file)
for name in ["README.md","AGENTS.md","PROGRESS.md","package.json","pnpm-lock.yaml",
             "pnpm-workspace.yaml","requirements.txt",".gitignore",
             "knowledge-prompt(1).md","凸优化系统学习笔记.md","凸优化从零开始学习笔记.md"]:
    files.append(ROOT/name)
out=ROOT/"凸优化教材项目.zip"
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as archive:
    for file in sorted(set(files)):
        archive.write(file,file.relative_to(ROOT).as_posix())
with zipfile.ZipFile(out) as archive:
    assert archive.testzip() is None
print(json.dumps({"files":len(set(files)),"bytes":out.stat().st_size,"download_anchors":"passed"}))
