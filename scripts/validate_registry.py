#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys, yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry/books.yaml"
SCHEMA = ROOT / "registry/schema-v2.json"
INDEX = ROOT / "books/index.yaml"

def y(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def main():
    errors = []
    reg, idx = y(REGISTRY), y(INDEX)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    for e in sorted(Draft202012Validator(schema).iter_errors(reg), key=lambda e: list(e.absolute_path)):
        p = ".".join(map(str, e.absolute_path)) or "<root>"
        errors.append(f"V08 schema violation at {p}: {e.message}")

    if "reading_rag_status" in reg:
        errors.append("legacy reading_rag_status is forbidden in registry v2")

    source = reg.get("source") or {}
    source_rel = source.get("file")
    if source_rel:
        source_path = ROOT / source_rel
        if not source_path.is_file():
            errors.append(f"V11 registry source snapshot missing: {source_rel}")
        else:
            actual_size = source_path.stat().st_size
            if source.get("size_bytes") != actual_size:
                errors.append(
                    f"V12 registry source snapshot size mismatch: "
                    f"expected {source.get('size_bytes')}, got {actual_size}"
                )
            actual_sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
            if source.get("sha256") != actual_sha:
                errors.append(
                    f"V13 registry source snapshot SHA-256 mismatch: "
                    f"expected {source.get('sha256')}, got {actual_sha}"
                )

    books = reg.get("books") or []
    numbers = [b.get("number") for b in books]
    number_dup = sorted({x for x in numbers if numbers.count(x) > 1})
    if number_dup:
        errors.append(f"V15 duplicate book number: {number_dup}")

    inv = [b.get("inventory_number") for b in books]
    invset = set(inv)
    dup = sorted({x for x in inv if inv.count(x) > 1})
    if dup:
        errors.append(f"V01 duplicate inventory_number: {dup}")
    if (reg.get("scope") or {}).get("book_count") != len(books):
        errors.append("V02 scope.book_count does not equal len(books)")

    index_books = idx.get("books") or []
    index_by_id = {b["id"]: b for b in index_books}

    allowed_project_status = {"planned", "in_progress", "completed", "frozen"}
    for item in index_books:
        project_status = item.get("project_status")
        if project_status is not None and project_status not in allowed_project_status:
            errors.append(
                f"V16 invalid project_status {project_status!r} for {item.get('id')}"
            )
        if project_status == "completed":
            if item.get("project_status_evidence") != "user_chat_plus":
                errors.append(
                    f"V17 completed project lacks user_chat_plus evidence: {item.get('id')}"
                )
            confirmed_at = item.get("project_status_confirmed_at")
            if not isinstance(confirmed_at, str) or len(confirmed_at) != 10:
                errors.append(
                    f"V18 completed project lacks YYYY-MM-DD confirmation date: {item.get('id')}"
                )

    kids = [b["knowledge_id"] for b in books if b.get("knowledge_id")]
    for b in books:
        kid = b.get("knowledge_id")
        if kid and kid not in index_by_id:
            errors.append(f"V06 dangling knowledge_id {kid!r} from {b.get('inventory_number')}")
    kd = sorted({x for x in kids if kids.count(x) > 1})
    if kd:
        errors.append(f"V07 conflicting knowledge_id mappings: {kd}")

    eh = reg.get("electronic_holdings") or {}
    holdings = eh.get("files") or []
    actual_matched = sum(1 for h in holdings if h.get("match_status") == "matched")
    actual_needs_confirmation = sum(
        1 for h in holdings
        if h.get("match_status") in {"ambiguous", "needs_confirmation"}
    )
    actual_unregistered = sum(
        1 for h in holdings if h.get("match_status") == "unregistered"
    )
    declared_counts = {
        "file_count": len(holdings),
        "matched_unambiguous": actual_matched,
        "needs_confirmation": actual_needs_confirmation,
        "unregistered": actual_unregistered,
    }
    for field, actual in declared_counts.items():
        if eh.get(field) != actual:
            errors.append(
                f"V14 electronic_holdings.{field} mismatch: "
                f"expected {eh.get(field)}, actual {actual}"
            )

    inv_by_number = {b.get("inventory_number"): b for b in books}
    for i, h in enumerate(holdings):
        refs = h.get("inventory_numbers") or []
        missing = sorted(set(refs) - invset)
        if missing:
            errors.append(f"V03 holdings[{i}] unknown inventory: {missing}")
        if h.get("match_status") == "matched" and not refs:
            errors.append(f"V04 matched holding has no inventory: {h.get('filename')}")
        if h.get("match_status") == "unregistered" and refs:
            errors.append(f"V05 unregistered holding has inventory: {h.get('filename')}")

        holding_kid = h.get("knowledge_id")
        if holding_kid and holding_kid not in index_by_id:
            errors.append(
                f"V09 holdings[{i}] dangling knowledge_id {holding_kid!r}: {h.get('filename')}"
            )
        if holding_kid and refs:
            linked_inventory_kids = {
                (inv_by_number.get(inv) or {}).get("knowledge_id")
                for inv in refs
                if (inv_by_number.get(inv) or {}).get("knowledge_id")
            }
            if linked_inventory_kids and holding_kid not in linked_inventory_kids:
                errors.append(
                    f"V10 holding knowledge_id {holding_kid!r} conflicts with inventory mapping "
                    f"{sorted(linked_inventory_kids)}: {h.get('filename')}"
                )

    for kid, item in index_by_id.items():
        paths = item.get("paths") or {}
        rp = paths.get("reading_progress")
        if rp:
            path = ROOT / rp
            if not path.is_file():
                errors.append(f"missing reading_progress for {kid}: {rp}")
            elif (y(path) or {}).get("book_id") != kid:
                errors.append(f"reading_progress book_id mismatch for {kid}")
            else:
                pair = (y(path) or {}).get("paired_reading")
                if isinstance(pair, dict) and pair.get("book_id") not in index_by_id:
                    errors.append(f"paired_reading from {kid} references unknown book_id")
        rm = paths.get("rag_manifest")
        if rm:
            path = ROOT / rm
            if not path.is_file():
                errors.append(f"missing rag_manifest for {kid}: {rm}")
            elif (y(path) or {}).get("book_id") != kid:
                errors.append(f"rag_manifest book_id mismatch for {kid}")

    if errors:
        for e in errors:
            print("ERROR:", e, file=sys.stderr)
        return 1
    print(f"registry validation OK: {len(books)} inventory, {len(kids)} knowledge mappings, {len(holdings)} holdings")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
