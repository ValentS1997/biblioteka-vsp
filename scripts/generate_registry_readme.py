#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/books.yaml"
INDEX = ROOT / "books/index.yaml"
OUTPUT = ROOT / "registry/README.md"

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

    progress, rags = {}, {}
    for kid, item in idx_by_id.items():
        paths = item.get("paths") or {}
        if paths.get("reading_progress") and (ROOT / paths["reading_progress"]).is_file():
            progress[kid] = y(ROOT / paths["reading_progress"])
        if paths.get("rag_manifest") and (ROOT / paths["rag_manifest"]).is_file():
            rags[kid] = y(ROOT / paths["rag_manifest"])

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
        "<!-- Source: registry/books.yaml + books/index.yaml + per-book reading/RAG manifests -->",
        "",
        "# Реестр библиотеки",
        "",
        "Канонический human-readable view. Архитектурный контракт: [`ARCHITECTURE.md`](./ARCHITECTURE.md).",
        "",
        f"> **{len(inventory_books)} инвентарных книг** · инвентарные номера `0001–0046` · **{reg['electronic_holdings']['file_count']} электронный файл** · актуально на `{reg['updated']}`",
    ]

    reverse = {}
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
