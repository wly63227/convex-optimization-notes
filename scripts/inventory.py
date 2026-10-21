"""Extract source evidence; page numbers are one-based PDF physical pages."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sources"
OUT.mkdir(exist_ok=True)
(OUT / "lecture-text").mkdir(exist_ok=True)
manifest = []
pages = []
for name, role in [("bv_cvxslides.pdf", "primary"), ("bv_cvxbook.pdf", "reference")]:
    path = ROOT / name
    reader = PdfReader(path)
    manifest.append({
        "file": name, "role": role, "pages": len(reader.pages),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "version": "local supplied file; see title/copyright page",
        "pdf_page_numbering": "physical, starting at 1",
    })
    if role != "primary":
        continue
    chapter = 0
    chunks = {}
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        lines = [s.strip() for s in text.splitlines() if s.strip()]
        title = lines[0] if lines else "(no extractable text)"
        match = re.match(r"^(\d+)\.\s+(.+)", title)
        if match and int(match[1]) <= 12:
            chapter = int(match[1])
        if title.startswith("B. Numerical linear algebra"):
            chapter = 13
        if title == "Convex Optimization" and i == 1:
            kind = "cover"
        elif match and len(lines) <= 3:
            kind = "chapter-cover"
        elif title == "Outline":
            kind = "outline"
        else:
            kind = "content"
        pages.append({
            "source": name, "page": i, "chapter": chapter,
            "title": title, "kind": kind, "text": text,
            "visual_review": "pending", "coverage": "pending",
        })
        chunks.setdefault(chapter, []).append(f"=== PDF PAGE {i}: {title} ===\n{text}")
    for ch, chunk in chunks.items():
        (OUT / "lecture-text" / f"{ch:02d}.txt").write_text("\n\n".join(chunk), encoding="utf-8")
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
for ch in sorted({p["chapter"] for p in pages}):
    group = [p for p in pages if p["chapter"] == ch]
    print(ch, group[0]["page"], group[-1]["page"], len(group), "pages", sum(len(p["text"]) for p in group), "characters")
