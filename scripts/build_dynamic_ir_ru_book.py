#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import yaml
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Mm, Pt

BOOK_ID = "dynamic-incident-response-joshua-wright-en-2026"
BOOK_TITLE_RU = "Динамическое реагирование на инциденты"
BOOK_SUBTITLE_RU = "Фреймворк для команд безопасности"
ORIGINAL_TITLE = "Dynamic Incident Response: A Framework for Security Teams"
AUTHOR = "Joshua Wright"
YEAR = "2026"
LICENSE = "CC BY 4.0"

def split_frontmatter(text: str):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            raw = text[4:end]
            body = text[end + 5:]
            try:
                data = yaml.safe_load(raw) or {}
                if isinstance(data, dict):
                    return data, body
            except yaml.YAMLError:
                data = {}
                for key in ("translation_status", "qa_status", "chapter_number", "source_title"):
                    m = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*(.+?)\s*$", raw)
                    if m:
                        value = m.group(1).strip()
                        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                            value = value[1:-1]
                        data[key] = value
                return data, body
    return {}, text

def chapter_num(path: Path) -> int:
    m = re.match(r"chapter-(\d{2})-", path.name)
    if not m:
        raise ValueError(f"Cannot parse chapter number: {path}")
    return int(m.group(1))

def normalize_body(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(
        r"^THIRD_PARTY_REVIEW_REQUIRED\s*[—-]\s*(.+)$",
        r"> **Примечание по правам:** материал третьей стороны не воспроизводится в этой версии. \1",
        text,
        flags=re.MULTILINE,
    )
    return text.strip() + "\n"

def build_reference_docx(path: Path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Mm(210)
    sec.page_height = Mm(297)
    sec.top_margin = Mm(18)
    sec.bottom_margin = Mm(18)
    sec.left_margin = Mm(19)
    sec.right_margin = Mm(17)
    sec.header_distance = Mm(8)
    sec.footer_distance = Mm(9)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Liberation Serif"
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Liberation Serif")
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.line_spacing = 1.08

    for name, size in [("Title", 28), ("Subtitle", 16), ("Heading 1", 20), ("Heading 2", 15), ("Heading 3", 12)]:
        st = styles[name]
        st.font.name = "Liberation Sans"
        st._element.rPr.rFonts.set(qn("w:eastAsia"), "Liberation Sans")
        st.font.size = Pt(size)
        if name == "Heading 1":
            st.paragraph_format.page_break_before = True
            st.paragraph_format.space_before = Pt(0)
            st.paragraph_format.space_after = Pt(10)

    for name in ["Code", "Source Code"]:
        if name in styles:
            st = styles[name]
            st.font.name = "Liberation Mono"
            st._element.rPr.rFonts.set(qn("w:eastAsia"), "Liberation Mono")
            st.font.size = Pt(8.5)

    # compact table style defaults via Normal font; pandoc handles grid borders.
    doc.save(path)

def audit_and_assemble(repo_root: Path, out_dir: Path):
    tr_root = repo_root / "books" / BOOK_ID / "translation" / "ru"
    chapters_dir = tr_root / "chapters"

    chapter_files = sorted(
        [p for p in chapters_dir.glob("chapter-*.md") if not p.name.endswith(".qa.md")],
        key=chapter_num,
    )
    qa_files = {chapter_num(p): p for p in chapters_dir.glob("chapter-*.qa.md")}

    nums = [chapter_num(p) for p in chapter_files]
    expected = list(range(1, 21))
    problems = []

    if nums != expected:
        problems.append(f"chapter sequence mismatch: got={nums}, expected={expected}")

    audit_rows = []
    third_party_flags = 0
    needs_confirmation = 0

    assembled_parts = []

    attribution_path = tr_root / "ATTRIBUTION.md"
    if not attribution_path.exists():
        problems.append("ATTRIBUTION.md missing")

    for p in chapter_files:
        n = chapter_num(p)
        raw = p.read_text(encoding="utf-8")
        meta, body = split_frontmatter(raw)
        status = meta.get("translation_status")
        if status != "ACCEPTED":
            problems.append(f"chapter {n}: translation_status={status!r}")

        qpath = qa_files.get(n)
        qstatus = None
        if not qpath:
            problems.append(f"chapter {n}: QA file missing")
        else:
            qmeta, _ = split_frontmatter(qpath.read_text(encoding="utf-8"))
            qstatus = qmeta.get("qa_status")
            if qstatus != "ACCEPTED":
                problems.append(f"chapter {n}: qa_status={qstatus!r}")

        tpc = body.count("THIRD_PARTY_REVIEW_REQUIRED")
        ncf = body.count("[Needs confirmation]")
        third_party_flags += tpc
        needs_confirmation += ncf
        if ncf:
            problems.append(f"chapter {n}: contains {ncf} [Needs confirmation] marker(s)")

        title = next((line.lstrip("# ").strip() for line in body.splitlines() if line.startswith("# ")), p.stem)
        audit_rows.append({
            "chapter": n,
            "file": p.name,
            "translation_status": status,
            "qa_status": qstatus,
            "title": title,
            "third_party_flags": tpc,
            "needs_confirmation": ncf,
        })
        assembled_parts.append(normalize_body(body))

    afterword = tr_root / "afterword.md"
    afterword_qa = tr_root / "afterword.qa.md"
    if not afterword.exists():
        problems.append("afterword.md missing")
    else:
        ameta, abody = split_frontmatter(afterword.read_text(encoding="utf-8"))
        if ameta.get("translation_status") != "ACCEPTED":
            problems.append(f"afterword translation_status={ameta.get('translation_status')!r}")
        third_party_flags += abody.count("THIRD_PARTY_REVIEW_REQUIRED")
        ncf = abody.count("[Needs confirmation]")
        needs_confirmation += ncf
        if ncf:
            problems.append(f"afterword contains {ncf} [Needs confirmation] marker(s)")
    if not afterword_qa.exists():
        problems.append("afterword.qa.md missing")
    else:
        aqmeta, _ = split_frontmatter(afterword_qa.read_text(encoding="utf-8"))
        if aqmeta.get("qa_status") != "ACCEPTED":
            problems.append(f"afterword qa_status={aqmeta.get('qa_status')!r}")

    audit = {
        "book_id": BOOK_ID,
        "status": "ACCEPTED" if not problems else "BLOCKED",
        "chapters_expected": 20,
        "chapters_found": len(chapter_files),
        "third_party_review_markers": third_party_flags,
        "needs_confirmation_markers": needs_confirmation,
        "problems": problems,
        "chapters": audit_rows,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "book-level-audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    report = [
        "# Book-level audit",
        "",
        f"- status: **{audit['status']}**",
        f"- chapters: {len(chapter_files)}/20",
        f"- third-party review markers preserved: {third_party_flags}",
        f"- [Needs confirmation] markers: {needs_confirmation}",
        "",
    ]
    if problems:
        report += ["## Blocking findings", ""] + [f"- {p}" for p in problems]
    else:
        report += ["## Result", "", "All numbered chapters and the Afterword satisfy the assembly gate."]
    (out_dir / "book-level-audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    if problems:
        raise SystemExit("Book-level audit BLOCKED:\n- " + "\n- ".join(problems))

    attribution = attribution_path.read_text(encoding="utf-8")
    _, attribution_body = split_frontmatter(attribution)

    glossary_path = tr_root / "glossary.yaml"
    glossary_md = ""
    if glossary_path.exists():
        gd = yaml.safe_load(glossary_path.read_text(encoding="utf-8")) or {}
        entries = gd.get("entries") or gd.get("terms") or []
        if isinstance(entries, list) and entries:
            lines = ["# Приложение. Глоссарий", "", "| English | Русский | Контекст |", "|---|---|---|"]
            for e in entries:
                if not isinstance(e, dict):
                    continue
                src = str(e.get("source", "")).replace("|", "\\|")
                ru = str(e.get("ru", "")).replace("|", "\\|")
                note = str(e.get("context_note", "")).replace("|", "\\|").replace("\n", " ")
                lines.append(f"| {src} | {ru} | {note} |")
            glossary_md = "\n".join(lines) + "\n"

    header = f"""---
title: "{BOOK_TITLE_RU}"
subtitle: "{BOOK_SUBTITLE_RU}"
author: "{AUTHOR}"
date: "{YEAR}"
lang: ru-RU
---

# Сведения об издании

**Оригинал:** *{ORIGINAL_TITLE}*  
**Автор:** {AUTHOR}  
**Издатель оригинала:** SANS Institute, {YEAR}  
**Лицензия основного авторского материала:** {LICENSE}  

Это **неофициальный русский перевод**. Он не является официальным изданием SANS Institute и не заявляет права на товарные знаки или сторонние материалы.

## Атрибуция и границы лицензии

{normalize_body(attribution_body)}

## Примечание к русскому изданию

В эту PDF-сборку включены принятые QA переводы глав 1-20 и послесловия. Оригинальный индекс не включён, поскольку его пагинация относится к английскому изданию и становится некорректной после русской перевёрстки.

Сторонние изображения, графики, screenshots и иные элементы, исключённые из основной лицензии CC BY 4.0, не воспроизводятся. На их месте сохранены текстовые пометки по правам и описания, когда они присутствуют в принятом переводе.

"""
    md = header + "\n\n".join(assembled_parts)
    if afterword.exists():
        _, abody = split_frontmatter(afterword.read_text(encoding="utf-8"))
        md += "\n\n" + normalize_body(abody)
    if glossary_md:
        md += "\n\n" + glossary_md

    md_path = out_dir / "dynamic-incident-response-ru.md"
    md_path.write_text(md, encoding="utf-8")
    return md_path, audit

def run_pandoc(md_path: Path, out_dir: Path):
    ref = out_dir / "reference.docx"
    build_reference_docx(ref)
    docx = out_dir / "dynamic-incident-response-ru-a4.docx"
    cmd = [
        "pandoc", str(md_path),
        "--from", "markdown+yaml_metadata_block",
        "--to", "docx",
        "--reference-doc", str(ref),
        "--toc",
        "--toc-depth=2",
        "--metadata", "toc-title=Оглавление",
        "--output", str(docx),
    ]
    subprocess.run(cmd, check=True)
    return docx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out-dir", default="build/dynamic-ir-ru-book")
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    md, audit = audit_and_assemble(repo_root, out_dir)
    docx = run_pandoc(md, out_dir)
    print(json.dumps({
        "status": audit["status"],
        "markdown": str(md),
        "docx": str(docx),
        "audit": str(out_dir / "book-level-audit.json"),
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
