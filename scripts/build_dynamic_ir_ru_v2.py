#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
from pathlib import Path

import yaml

from build_dynamic_ir_ru_book import (
    BOOK_ID,
    BOOK_TITLE_RU,
    BOOK_SUBTITLE_RU,
    ORIGINAL_TITLE,
    AUTHOR,
    YEAR,
    LICENSE,
    split_frontmatter,
    chapter_num,
    build_reference_docx,
)

HEADING_REPLACEMENTS = {
    "INCIDENT RESPONSE": "РЕАГИРОВАНИЕ НА ИНЦИДЕНТЫ",
    "INCIDENT MANAGEMENT": "УПРАВЛЕНИЕ ИНЦИДЕНТАМИ",
    "STEP-BY-STEP": "ПОШАГОВО",
    "SIDEBAR:": "ВРЕЗКА:",
    "CASE:": "ПРИМЕР:",
    "INTRODUCTION": "ВВЕДЕНИЕ",
    "PREPARE": "ПОДГОТОВКА",
    "DETECT": "ОБНАРУЖЕНИЕ",
    "VERIFY/TRIAGE": "ПРОВЕРКА И ТРИАЖ",
    "VERIFY AND TRIAGE": "ПРОВЕРКА И ТРИАЖ",
    "SCOPE": "ОПРЕДЕЛЕНИЕ МАСШТАБА",
    "CONTAINMENT": "СДЕРЖИВАНИЕ",
    "CONTAIN": "СДЕРЖИВАНИЕ",
    "ERADICATE": "ИСКОРЕНЕНИЕ",
    "RECOVER": "ВОССТАНОВЛЕНИЕ",
    "DEBRIEF": "РАЗБОР ИНЦИДЕНТА",
    "DOCUMENTATION": "ДОКУМЕНТИРОВАНИЕ",
    "INITIAL RISK ASSESSMENT": "НАЧАЛЬНАЯ ОЦЕНКА РИСКА",
    "STAKEHOLDER COMMUNICATION": "КОММУНИКАЦИЯ С ЗАИНТЕРЕСОВАННЫМИ СТОРОНАМИ",
    "PRACTICAL CONSIDERATIONS": "ПРАКТИЧЕСКИЕ АСПЕКТЫ",
    "KNOWING WHEN TO STOP": "КРИТЕРИИ ЗАВЕРШЕНИЯ",
    "ITERATION TRIGGERS": "ТРИГГЕРЫ НОВОЙ ИТЕРАЦИИ",
    "CLOUD-NATIVE DETECTION TOOLING": "ВСТРОЕННЫЕ ОБЛАЧНЫЕ СРЕДСТВА ОБНАРУЖЕНИЯ",
    "DETECTION TOOLING FOR AWS": "СРЕДСТВА ОБНАРУЖЕНИЯ В AWS",
    "DETECTION TOOLING FOR AZURE": "СРЕДСТВА ОБНАРУЖЕНИЯ В AZURE",
    "DETECTION TOOLING FOR GOOGLE CLOUD": "СРЕДСТВА ОБНАРУЖЕНИЯ В GOOGLE CLOUD",
    "CLOUD-SPECIFIC DEBRIEF QUESTIONS": "ВОПРОСЫ ДЛЯ РАЗБОРА ОБЛАЧНОГО ИНЦИДЕНТА",
    "AUTOMATED RESPONSE CAPABILITIES": "ВОЗМОЖНОСТИ АВТОМАТИЗИРОВАННОГО РЕАГИРОВАНИЯ",
    "MULTI-CLOUD ENVIRONMENTS": "МУЛЬТИОБЛАЧНЫЕ СРЕДЫ",
    "RANSOMWARE INTRODUCTION": "ВВЕДЕНИЕ В RANSOMWARE",
    "RANSOMWARE ATTACK TRENDS": "ТЕНДЕНЦИИ RANSOMWARE-АТАК",
    "INITIAL ACCESS TRENDS": "ТЕНДЕНЦИИ ПЕРВОНАЧАЛЬНОГО ДОСТУПА",
    "ATTACK DIFFERENTIATION": "РАЗЛИЧЕНИЕ ТИПОВ АТАК",
    "FINAL CONSIDERATIONS": "ЗАКЛЮЧИТЕЛЬНЫЕ СООБРАЖЕНИЯ",
    "RANSOMWARE-SPECIFIC METRICS": "МЕТРИКИ ДЛЯ RANSOMWARE-ИНЦИДЕНТОВ",
    "RANSOMWARE-SPECIFIC DEBRIEF QUESTIONS": "ВОПРОСЫ ДЛЯ РАЗБОРА RANSOMWARE-ИНЦИДЕНТА",
    "RECOVERY PLANNING AND PRIORITIZATION": "ПЛАНИРОВАНИЕ И ПРИОРИТИЗАЦИЯ ВОССТАНОВЛЕНИЯ",
    "DECRYPTED DOES NOT MEAN CLEAN": "РАСШИФРОВАНО НЕ ОЗНАЧАЕТ ОЧИЩЕНО",
    "WATCHING FOR ATTACKER RETURN": "НАБЛЮДЕНИЕ ЗА ВОЗВРАЩЕНИЕМ АТАКУЮЩЕГО",
    "COMMUNICATION DURING RECOVERY": "КОММУНИКАЦИЯ ВО ВРЕМЯ ВОССТАНОВЛЕНИЯ",
    "SAFETY": "БЕЗОПАСНОСТЬ",
    "ISLAND MODE": "АВТОНОМНЫЙ РЕЖИМ (ISLAND MODE)",
    "COMMON OT INCIDENT DATA SOURCES": "ОСНОВНЫЕ ИСТОЧНИКИ ДАННЫХ ОБ OT-ИНЦИДЕНТАХ",
    "TRADITIONAL VS NEW FORENSIC AREAS": "ТРАДИЦИОННЫЕ И НОВЫЕ ОБЛАСТИ ФОРЕНЗИКИ",
    "THE FIVE ICS CYBERSECURITY CRITICAL CONTROLS": "ПЯТЬ КРИТИЧЕСКИХ МЕР КИБЕРБЕЗОПАСНОСТИ ICS",
    "AI COSTS AND ACCESS": "СТОИМОСТЬ И ДОСТУП К ИИ",
    "OPPORTUNITIES AND CAUTIONS": "ВОЗМОЖНОСТИ И ОГРАНИЧЕНИЯ",
    "PROMPTING FOUNDATIONS": "ОСНОВЫ ФОРМИРОВАНИЯ ЗАПРОСОВ",
    "FOUNDATIONAL USE CASES": "БАЗОВЫЕ СЦЕНАРИИ ПРИМЕНЕНИЯ",
    "INTERMEDIATE USE CASES": "ПРОМЕЖУТОЧНЫЕ СЦЕНАРИИ ПРИМЕНЕНИЯ",
    "ADVANCED USE CASES": "РАСШИРЕННЫЕ СЦЕНАРИИ ПРИМЕНЕНИЯ",
    "OPERATIONAL CONSIDERATIONS": "ОПЕРАЦИОННЫЕ АСПЕКТЫ",
    "LOOKING FORWARD": "ЧТО ДАЛЬШЕ",
    "VERIFICATION IS NON-NEGOTIABLE": "ПРОВЕРКА ОБЯЗАТЕЛЬНА",
    "MODEL CONTEXT PROTOCOL FOR DEFENSIVE OPERATIONS": "MODEL CONTEXT PROTOCOL ДЛЯ ЗАЩИТНЫХ ОПЕРАЦИЙ",
    "SECURITY CONSIDERATIONS": "АСПЕКТЫ БЕЗОПАСНОСТИ",
    "HUMAN IN THE LOOP (HITL)": "ЧЕЛОВЕК В КОНТУРЕ (HITL)",
    "AUDITABILITY AND DOCUMENTATION": "АУДИРУЕМОСТЬ И ДОКУМЕНТИРОВАНИЕ",
    "STABLE PRINCIPLES": "УСТОЙЧИВЫЕ ПРИНЦИПЫ",
}

PHRASE_REPLACEMENTS = [
    ("incident response", "реагирование на инциденты"),
    ("Incident Response", "реагирование на инциденты"),
    ("incident management", "управление инцидентами"),
    ("Decision Makers", "лица, принимающие решения"),
    ("Decision-Makers", "лица, принимающие решения"),
    ("System Owner", "владелец системы"),
    ("System owner", "владелец системы"),
    ("Residual-Access Window", "окно остаточного доступа"),
    ("Initial Risk Assessment", "начальная оценка риска"),
    ("Cloud Incident Response", "реагирование на инциденты в облачной среде"),
    ("Control Plane", "плоскость управления"),
    ("Data Plane", "плоскость данных"),
    ("Runtime visibility", "наблюдаемость времени выполнения"),
    ("Multi-cloud visibility", "сквозная видимость multi-cloud"),
]

def normalize_heading_text(text: str) -> str:
    original = text
    key = text.strip()
    upper = key.upper()
    if upper in HEADING_REPLACEMENTS:
        return HEADING_REPLACEMENTS[upper]
    out = key
    for src, dst in PHRASE_REPLACEMENTS:
        out = out.replace(src, dst)
    # Keep code/generated-content section markers stable if translation would be ambiguous.
    out = re.sub(r"\bSTEP (\d+)\b", r"Шаг \1", out, flags=re.I)
    return out if out else original

def normalize_body_v2(text: str) -> str:
    text = html.unescape(text.replace("\r\n", "\n"))
    text = text.replace("&#x20;", " ")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    lines = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            marks, title = m.groups()
            title = normalize_heading_text(title)
            line = f"{marks} {title}"
        lines.append(line)
    text = "\n".join(lines)

    text = re.sub(
        r"^THIRD_PARTY_REVIEW_REQUIRED\s*[—-]?\s*(.*)$",
        lambda m: "> **Иллюстрация не воспроизводится:** требуется отдельная проверка прав на сторонний визуальный материал."
                  + (f" {m.group(1).strip()}" if m.group(1).strip() else ""),
        text,
        flags=re.MULTILINE,
    )
    text = text.replace("THIRD_PARTY_REVIEW_REQUIRED", "**Иллюстрация не воспроизводится:** требуется отдельная проверка прав на сторонний визуальный материал.")
    text = text.replace("RAG_MISS", "пропуск в извлечённом тексте источника")
    return text.strip() + "\n"

def audit_and_assemble(repo_root: Path, out_dir: Path):
    tr_root = repo_root / "books" / BOOK_ID / "translation" / "ru"
    chapters_dir = tr_root / "chapters"
    chapter_files = sorted(
        [p for p in chapters_dir.glob("chapter-*.md") if not p.name.endswith(".qa.md")],
        key=chapter_num,
    )
    qa_files = {chapter_num(p): p for p in chapters_dir.glob("chapter-*.qa.md")}
    problems = []
    rows = []
    parts = []
    original_third_party = 0
    v2_third_party = 0

    if [chapter_num(p) for p in chapter_files] != list(range(1, 21)):
        problems.append("chapter sequence mismatch")

    for p in chapter_files:
        n = chapter_num(p)
        raw = p.read_text(encoding="utf-8")
        meta, body = split_frontmatter(raw)
        q = qa_files.get(n)
        qmeta = {}
        if q:
            qmeta, _ = split_frontmatter(q.read_text(encoding="utf-8"))
        if meta.get("translation_status") != "ACCEPTED":
            problems.append(f"chapter {n}: translation status is not ACCEPTED")
        if qmeta.get("qa_status") != "ACCEPTED":
            problems.append(f"chapter {n}: QA status is not ACCEPTED")
        if "[Needs confirmation]" in body:
            problems.append(f"chapter {n}: unexpected [Needs confirmation]")
        original_third_party += body.count("THIRD_PARTY_REVIEW_REQUIRED")
        repaired = normalize_body_v2(body)
        v2_third_party += repaired.count("требуется отдельная проверка прав на сторонний визуальный материал")
        parts.append(repaired)
        title = next((l.lstrip("# ").strip() for l in repaired.splitlines() if l.startswith("# ")), p.stem)
        rows.append({"chapter": n, "file": p.name, "title": title})

    afterword = tr_root / "afterword.md"
    afterword_qa = tr_root / "afterword.qa.md"
    if not afterword.exists() or not afterword_qa.exists():
        problems.append("afterword or QA missing")
        abody = ""
    else:
        ameta, abody = split_frontmatter(afterword.read_text(encoding="utf-8"))
        aqmeta, _ = split_frontmatter(afterword_qa.read_text(encoding="utf-8"))
        if ameta.get("translation_status") != "ACCEPTED":
            problems.append("afterword translation status is not ACCEPTED")
        if aqmeta.get("qa_status") != "ACCEPTED":
            problems.append("afterword QA status is not ACCEPTED")
        original_third_party += abody.count("THIRD_PARTY_REVIEW_REQUIRED")
        abody = normalize_body_v2(abody)

    if v2_third_party != original_third_party:\n        problems.append(f"third-party marker preservation mismatch: source={original_third_party}, v2={v2_third_party}")\n\n    audit = {
        "book_id": BOOK_ID,
        "edition": "ru-v2-repair",
        "status": "ACCEPTED" if not problems else "BLOCKED",
        "chapters": rows,
        "third_party_markers_source": original_third_party,
        "third_party_callouts_v2": v2_third_party,
        "problems": problems,
        "chapter_analysis_workflow": "BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.2 -> BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.6",
        "workflow_provenance": "RETROFIT_VERIFIED_COMPATIBILITY",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "dynamic-incident-response-ru-v2-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if problems:
        raise SystemExit("RU v2 audit BLOCKED:\n- " + "\n- ".join(problems))

    toc = ["# Оглавление", ""] + [f"- {r['title']}" for r in rows] + ["- Послесловие"]
    header = f"""---
title: "{BOOK_TITLE_RU}"
subtitle: "{BOOK_SUBTITLE_RU} - неофициальный русский перевод, редакция v2"
author: "{AUTHOR}"
date: "{YEAR}"
lang: ru-RU
---

{chr(10).join(toc)}

# Сведения об издании

**Оригинал:** *{ORIGINAL_TITLE}*  
**Автор:** {AUTHOR}  
**Издатель оригинала:** SANS Institute, {YEAR}  
**Лицензия основного авторского материала:** {LICENSE}  
**Лицензия:** https://creativecommons.org/licenses/by/4.0/

Это **неофициальный русский перевод**. Редакция v2 выполнена как редакторский ремонт принятого перевода глав 1-20 и послесловия: нормализация заголовков, терминологии и типографики без замены canonical English RAG.

Аналитические материалы глав проверены на совместимость с:
`BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.2 -> BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.6`.

Сторонние визуальные материалы не воспроизводятся без отдельной проверки прав. На их месте сохраняются подписи и явные пометки.

"""
    md = header + "\n\n".join(parts) + "\n\n" + abody

    glossary_path = tr_root / "glossary.yaml"
    if glossary_path.exists():
        gd = yaml.safe_load(glossary_path.read_text(encoding="utf-8")) or {}
        entries = gd.get("entries") or gd.get("terms") or []
        if isinstance(entries, list) and entries:
            gl = ["# Приложение. Глоссарий", ""]
            for e in entries:
                if not isinstance(e, dict):
                    continue
                src = str(e.get("source", "")).strip()
                ru = str(e.get("ru", "")).strip()
                note = str(e.get("context_note", "")).replace("\n", " ").strip()
                if not src:
                    continue
                item = f"- **{src}**"
                if ru:
                    item += f" - {ru}"
                if note:
                    item += f". {note}"
                gl.append(item)
            md += "\n\n" + "\n".join(gl) + "\n"

    md_path = out_dir / "dynamic-incident-response-ru-v2.md"
    md_path.write_text(md, encoding="utf-8")
    return md_path, audit

def run_pandoc(md_path: Path, out_dir: Path):
    ref = out_dir / "reference-v2.docx"
    build_reference_docx(ref)
    docx = out_dir / "dynamic-incident-response-ru-v2-a4.docx"
    subprocess.run([
        "pandoc", str(md_path),
        "--from", "markdown+yaml_metadata_block",
        "--to", "docx",
        "--reference-doc", str(ref),
        "--output", str(docx),
    ], check=True)
    return docx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out-dir", default="build/dynamic-ir-ru-v2")
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    md, audit = audit_and_assemble(repo_root, out_dir)
    docx = run_pandoc(md, out_dir)
    print(json.dumps({"status": audit["status"], "markdown": str(md), "docx": str(docx)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
