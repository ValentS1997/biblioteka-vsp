#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/books.yaml"
INDEX = ROOT / "books/index.yaml"
OUTPUT = ROOT / "registry/README.md"

PRIMARY_EXTRACT_NAMES = {
    "cheatsheet.md",
    "summary.md",
    "commands.md",
    "diagram.md",
    "visual-cheatsheet.svg",
    "visual-cheatsheet-detailed.svg",
    "final-conclusion.md",
    "book-summary.md",
    "synthesis.md",
}

def y(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def esc(v):
    return str(v).replace("|", "\\|").replace("\n", " ")

def read_label(status):
    return {"completed": "Да", "in_progress": "В процессе"}.get(status, "—")

def reading_date_label(value):
    if not isinstance(value, dict):
        return "—"
    exact = value.get("exact_date")
    month = value.get("month")
    if exact and exact != "[Needs confirmation]":
        return str(exact)
    if month and month != "[Needs confirmation]":
        return str(month)
    if exact == "[Needs confirmation]" or month == "[Needs confirmation]":
        return "[Needs confirmation]"
    return "—"

def rag_label(m):
    if not m:
        return "—"
    status = ((m.get("validation") or {}).get("status") or "")
    return "Да" if status.startswith("READY") else "⚠️"

def project_label(item):
    return "Завершено" if item.get("project_status") == "completed" else "[Needs confirmation]"

def extract_info(item):
    paths = item.get("paths") or {}
    notes_rel = paths.get("notes")
    if not notes_rel:
        return {"has": False, "chapter_count": 0, "artifact_count": 0}
    notes_root = ROOT / notes_rel
    if not notes_root.is_dir():
        return {"has": False, "chapter_count": 0, "artifact_count": 0}

    artifacts = [
        path for path in notes_root.rglob("*")
        if path.is_file() and path.name in PRIMARY_EXTRACT_NAMES
    ]
    chapter_dirs = set()
    for path in artifacts:
        rel = path.relative_to(notes_root)
        parts = rel.parts
        if len(parts) >= 3 and parts[0] == "chapters":
            chapter_dirs.add(parts[1])

    chapter_index = notes_root / "chapters" / "README.md"
    synthesis_index = notes_root / "book-synthesis" / "README.md"
    if chapter_dirs:
        landing = chapter_index if chapter_index.is_file() else notes_root / "chapters"
    elif synthesis_index.is_file() and artifacts:
        landing = synthesis_index
    else:
        landing = sorted(artifacts)[0] if artifacts else None

    return {
        "has": bool(artifacts),
        "chapter_count": len(chapter_dirs),
        "artifact_count": len(artifacts),
        "landing_path": landing.relative_to(ROOT).as_posix() if landing else None,
    }

def extracts_label(info):
    if not info.get("has"):
        return "—"
    chapter_count = int(info.get("chapter_count") or 0)
    label = f"Да ({chapter_count} гл.)" if chapter_count else "Да"
    landing_path = info.get("landing_path")
    return f"[{label}](../{landing_path})" if landing_path else label

def inventory_number_label(books):
    values = [str(b["inventory_number"]) for b in books]
    if not values:
        return "—"
    width = max(len(v) for v in values)
    nums = [int(v) for v in values]
    runs = []
    start = prev = nums[0]
    for value in nums[1:]:
        if value == prev + 1:
            prev = value
            continue
        runs.append((start, prev))
        start = prev = value
    runs.append((start, prev))
    parts = []
    for first, last in runs:
        if first == last:
            parts.append(f"{first:0{width}d}")
        else:
            parts.append(f"{first:0{width}d}–{last:0{width}d}")
    return ", ".join(parts)

def render():
    reg, idx = y(REGISTRY), y(INDEX)
    idx_by_id = {b["id"]: b for b in idx.get("books", [])}
    holdings = reg["electronic_holdings"]["files"]

    electronic = {}
    for h in holdings:
        for inv in h.get("inventory_numbers", []):
            electronic.setdefault(inv, []).append(h)

    def elabel(inv):
        items = electronic.get(inv, [])
        if not items:
            return "—"
        fmts, uncertain = [], False
        for h in items:
            f = str(h.get("format", "")).upper()
            if f and f not in fmts:
                fmts.append(f)
            uncertain |= h.get("match_status") != "matched"
        label = "/".join(fmts) or "—"
        return f"⚠️ {label}" if uncertain and label != "—" else label

    def has_pdf(inv):
        return any(
            str(h.get("format", "")).lower() == "pdf"
            and h.get("match_status") == "matched"
            for h in electronic.get(inv, [])
        )

    progress, rags, extracts = {}, {}, {}
    for kid, item in idx_by_id.items():
        paths = item.get("paths") or {}
        if paths.get("reading_progress") and (ROOT / paths["reading_progress"]).is_file():
            progress[kid] = y(ROOT / paths["reading_progress"])
        if paths.get("rag_manifest") and (ROOT / paths["rag_manifest"]).is_file():
            rags[kid] = y(ROOT / paths["rag_manifest"])
        extracts[kid] = extract_info(item)

    inventory_books = tuple(sorted(reg["books"], key=lambda b: b["number"]))
    expected_inventory_count = reg["scope"]["book_count"]
    if len(inventory_books) != expected_inventory_count:
        raise ValueError(
            "registry invariant failed: "
            f"scope.book_count={expected_inventory_count}, "
            f"inventory rows={len(inventory_books)}"
        )

    lines = [
        "<!-- GENERATED FILE. DO NOT EDIT MANUALLY. -->",
        "<!-- Source: registry/books.yaml + books/index.yaml + per-book reading/RAG manifests + notes artifacts -->",
        "",
        "# Реестр библиотеки",
        "",
        "Канонический human-readable view. Архитектурный контракт: [`ARCHITECTURE.md`](./ARCHITECTURE.md).",
        "",
        f"> **{len(inventory_books)} инвентарных книг** · инвентарные номера `{inventory_number_label(inventory_books)}` · **{reg['electronic_holdings']['file_count']} электронный файл** · актуально на `{reg['updated']}`",
    ]

    reverse = {
        b["knowledge_id"]: b["inventory_number"]
        for b in inventory_books
        if b.get("knowledge_id")
    }
    completed = active = rag_ready = 0

    reading_now = []
    reading_completed = []
    pdf_needed = []

    for b in inventory_books:
        inv, kid = b["inventory_number"], b.get("knowledge_id")
        p = progress.get(kid) if kid else None
        status = (p or {}).get("status")
        started = reading_date_label((p or {}).get("started")) if p else "—"
        finished = reading_date_label((p or {}).get("completed")) if p else "—"
        rg = rag_label(rags.get(kid) if kid else None)

        if status == "in_progress":
            reading_now.append((inv, b["title"], started, rg))
        elif status == "completed":
            reading_completed.append((inv, b["title"], started, finished, rg))

        if not has_pdf(inv):
            pdf_needed.append((inv, b["title"], elabel(inv)))

    if reading_now:
        lines += [
            "", "## Сейчас читаю", "",
            "| Инв. № | Название | Начал читать | Есть RAG |",
            "|:---:|---|:---:|:---:|",
        ]
        for inv, title, started, rg in reading_now:
            lines.append(f"| `{inv}` | **{esc(title)}** | {started} | {rg} |")

    if reading_completed:
        lines += [
            "", "## Прочитано", "",
            "| Инв. № | Название | Начал читать | Закончил читать | Есть RAG |",
            "|:---:|---|:---:|:---:|:---:|",
        ]
        for inv, title, started, finished, rg in reading_completed:
            lines.append(
                f"| `{inv}` | **{esc(title)}** | {started} | {finished} | {rg} |"
            )

    if pdf_needed:
        lines += [
            "", "## Нужен PDF", "",
            "Книги inventory, для которых нет однозначно сопоставленного electronic holding формата PDF.",
            "",
            "| Инв. № | Название | Известная электронная версия |",
            "|:---:|---|:---:|",
        ]
        for inv, title, electronic_label in pdf_needed:
            lines.append(
                f"| `{inv}` | **{esc(title)}** | {electronic_label} |"
            )

    knowledge_rows = []
    for kid, item in idx_by_id.items():
        inv = reverse.get(kid, "—")
        project = project_label(item)
        rg = rag_label(rags.get(kid))
        ex = extracts_label(extracts.get(kid) or {})
        sort_inv = int(inv) if inv != "—" and str(inv).isdigit() else 10**9
        knowledge_rows.append((sort_inv, str(inv), kid, item.get("title", kid), project, rg, ex))

    knowledge_rows.sort(key=lambda row: (row[0], row[3].lower(), row[2]))

    lines += [
        "", "## Покрытие knowledge-проектов", "",
        "Показывает состояние артефактов, которые реально находятся в `main`. "
        "`Проект` — подтверждённый пользователем статус книжного чата; "
        "`Есть RAG` — derived из `rag/manifest.yaml`; "
        "`Выжимки` — derived из фактических study artifacts в `notes/`; "
        "при наличии материалов значение ведёт к их списку.",
        "",
        "| Инв. № | Knowledge ID | Книга | Проект | Есть RAG | Выжимки |",
        "|:---:|---|---|:---:|:---:|:---:|",
    ]
    for _, inv, kid, title, project, rg, ex in knowledge_rows:
        inv_label = f"`{inv}`" if inv != "—" else "—"
        lines.append(
            f"| {inv_label} | `{esc(kid)}` | **{esc(title)}** | {project} | {rg} | {ex} |"
        )

    migration_gaps = []
    for _, inv, kid, title, project, rg, ex in knowledge_rows:
        if project != "Завершено":
            continue
        missing = []
        if rg != "Да":
            missing.append("RAG")
        if ex == "—":
            missing.append("выжимки")
        if missing:
            migration_gaps.append((inv, kid, title, ", ".join(missing)))

    lines += [
        "", "## Migration gaps", "",
        "Pre-transfer audit завершённых knowledge-проектов: проверяется наличие RAG и study/extract artifacts в текущем `main`.",
        "",
    ]
    if migration_gaps:
        lines += [
            "| Инв. № | Knowledge ID | Книга | Отсутствует в main |",
            "|:---:|---|---|---|",
        ]
        for inv, kid, title, missing in migration_gaps:
            inv_label = f"`{inv}`" if inv != "—" else "—"
            lines.append(
                f"| {inv_label} | `{esc(kid)}` | **{esc(title)}** | {esc(missing)} |"
            )
    else:
        lines.append("**Не обнаружены.** Все проекты со статусом `completed` имеют RAG и выжимки в текущем checkout.")

    lines += [
        "", "## Реестр книг", "",
        f"**Инвариант:** эта таблица всегда содержит весь inventory — {len(inventory_books)}/{expected_inventory_count} позиций. Дополнительные разделы выше и ниже являются только представлениями и не исключают книги из реестра.",
        "",
        "Обозначения: `Эл.` — известная электронная версия; `Прочитано`, `Начал читать` и `Закончил читать` — derived из `books/<knowledge-id>/reading/progress.yaml`; `Есть RAG` — derived из `books/<knowledge-id>/rag/manifest.yaml`.",
        "",
        "| № | Инв. № | Название | Начал читать | Закончил читать | Есть RAG | Прочитано | Эл. | Кратко | Направление | Автор(ы) | Перевод / редактура |",
        "|---:|:------:|---|:---:|:---:|:---:|:---:|:---:|---|---|---|---|",
    ]

    for b in inventory_books:
        inv, kid = b["inventory_number"], b.get("knowledge_id")
        if kid:
            reverse[kid] = inv
        p = progress.get(kid) if kid else None
        rd = read_label((p or {}).get("status"))
        if rd == "Да": completed += 1
        if rd == "В процессе": active += 1
        started = reading_date_label((p or {}).get("started")) if p else "—"
        finished = reading_date_label((p or {}).get("completed")) if p else "—"
        rg = rag_label(rags.get(kid) if kid else None)
        if rg == "Да": rag_ready += 1
        lines.append(
            f"| {b['number']} | `{inv}` | **{esc(b['title'])}** | "
            f"{started} | {finished} | {rg} | {rd} | {elabel(inv)} | "
            f"{esc(b['summary_short'])} | {esc(b['direction'])} | "
            f"{esc(b['authors_raw'])} | {esc(b['translators_editors_raw'])} |"
        )

    pairs = set()
    for kid, p in progress.items():
        pair = p.get("paired_reading")
        if isinstance(pair, dict) and pair.get("book_id") in idx_by_id:
            pairs.add(tuple(sorted((kid, pair["book_id"]))))
    if pairs:
        lines += ["", "## Связки чтения", ""]
        for a, b in sorted(pairs):
            lines.append(
                f"- `{reverse.get(a, '[Needs confirmation]')}` **{esc(idx_by_id[a].get('title', a))}** ↔ "
                f"`{reverse.get(b, '[Needs confirmation]')}` **{esc(idx_by_id[b].get('title', b))}** — читать в паре."
            )

    unregistered = [h for h in holdings if h.get("match_status") == "unregistered"]
    if unregistered:
        lines += [
            "", "## Электронные книги без инвентарного номера", "",
            "| Файл | Формат | Knowledge ID | Инв. № |",
            "|---|:---:|---|:---:|",
        ]
        for h in unregistered:
            kid = h.get("knowledge_id")
            kid_label = f"`{esc(kid)}`" if kid else "[Needs confirmation]"
            lines.append(
                f"| `{esc(h['filename'])}` | {str(h['format']).upper()} | "
                f"{kid_label} | [Needs confirmation] |"
            )

    uncertain = [h for h in holdings if h.get("match_status") in {"ambiguous", "needs_confirmation"}]
    if uncertain:
        lines += ["", "## Неоднозначные сопоставления", "", "| Позиция | Статус | Причина |", "|---|:---:|---|"]
        for h in uncertain:
            refs = " / ".join(f"`{x}`" for x in h.get("inventory_numbers", [])) or "—"
            lines.append(f"| {refs} | ⚠️ {str(h['format']).upper()} | {esc(h.get('note', '[Needs confirmation]'))} |")

    src, eh = reg["source"], reg["electronic_holdings"]
    inventory_knowledge_mappings = sum(1 for b in inventory_books if b.get("knowledge_id"))
    knowledge_entries = len(idx_by_id)
    knowledge_without_inventory = len(set(idx_by_id) - set(reverse))
    knowledge_rag_ready = sum(1 for m in rags.values() if rag_label(m) == "Да")
    project_completed = sum(
        1 for item in idx_by_id.values()
        if item.get("project_status") == "completed"
    )
    knowledge_with_extracts = sum(
        1 for info in extracts.values()
        if info.get("has")
    )
    completed_missing_rag = sum(
        1 for kid, item in idx_by_id.items()
        if item.get("project_status") == "completed" and rag_label(rags.get(kid)) != "Да"
    )
    completed_missing_extracts = sum(
        1 for kid, item in idx_by_id.items()
        if item.get("project_status") == "completed" and not (extracts.get(kid) or {}).get("has")
    )
    lines += [
        "", "## Контроль", "", "| Параметр | Значение |", "|---|---:|",
        f"| Инвентарных книг | **{len(inventory_books)}** |",
        f"| Inventory → knowledge mappings | **{inventory_knowledge_mappings}** |",
        f"| Knowledge entries всего | **{knowledge_entries}** |",
        f"| Knowledge entries без inventory | **{knowledge_without_inventory}** |",
        f"| Электронных файлов | **{eh['file_count']}** |",
        f"| Однозначно сопоставлено | **{eh['matched_unambiguous']}** |",
        f"| Требует подтверждения | **{eh['needs_confirmation']}** |",
        f"| Вне inventory | **{eh['unregistered']}** |",
        f"| Прочитано | **{completed}** |",
        f"| В процессе | **{active}** |",
        f"| RAG READY (inventory-linked) | **{rag_ready}** |",
        f"| RAG READY (knowledge total) | **{knowledge_rag_ready}** |",
        f"| Проектов завершено (user-confirmed '+') | **{project_completed}** |",
        f"| Knowledge entries с выжимками | **{knowledge_with_extracts}** |",
        f"| Завершено, но RAG отсутствует в main | **{completed_missing_rag}** |",
        f"| Завершено, но выжимки отсутствуют в main | **{completed_missing_extracts}** |",
        f"| SHA-256 Excel snapshot | `{src['sha256']}` |",
        f"| Размер Excel snapshot | `{src['size_bytes']} bytes` |",
        "", "README генерируется автоматически. Для изменения статусов правьте только canonical sources.", ""
    ]
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    out = render()
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != out:
            print("registry/README.md is stale; run: python scripts/generate_registry_readme.py", file=sys.stderr)
            return 1
        print("registry/README.md is up to date")
        return 0
    OUTPUT.write_text(out, encoding="utf-8")
    print("wrote registry/README.md")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
