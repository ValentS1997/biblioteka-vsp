#!/usr/bin/env python3
"""Report chapter publication from committed individual Git files (not chat/ZIP).

Chapter total is available only from a verified, committed RAG-grounded plan.
Run in a repository checkout at the intended book branch/commit:
  python scripts/chapter_publication_status.py --book-id <book_id>
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import yaml

REQUIRED = (
    "README.md", "cheatsheet.md", "commands.md", "diagram.md",
    "visual-cheatsheet.svg", "visual-cheatsheet-detailed.svg",
)
CHAPTER_RE = re.compile(r"^chapter-(\d+)-[A-Za-z0-9][A-Za-z0-9-]*$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")


def committed_paths(root: Path, prefix: str) -> set[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "--name-only", "HEAD", "--", prefix],
        capture_output=True, text=True, check=True,
    )
    return set(completed.stdout.splitlines())


def get_progress(root: Path, book_id: str) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", book_id):
        raise ValueError("Invalid book_id")
    root = root.resolve()
    book = root / "books" / book_id
    if not book.is_dir():
        raise ValueError(f"Book not found: {book_id}")
    prefix = f"books/{book_id}/notes/chapters"
    paths = committed_paths(root, prefix)
    complete, partial = set(), set()
    chapter_dirs: dict[int, set[str]] = {}
    for path in paths:
        parts = path.split("/")
        if len(parts) != 6 or "/".join(parts[:4]) != prefix:
            continue
        match = CHAPTER_RE.fullmatch(parts[4])
        if match:
            chapter_dirs.setdefault(int(match.group(1)), set()).add(parts[5])
    for number, filenames in chapter_dirs.items():
        (complete if set(REQUIRED).issubset(filenames) else partial).add(number)

    plan_rel = f"{prefix}/plan.yaml"
    total = None
    toc_evidence = None
    reason = "No committed, verified chapter plan; inspect canonical RAG TOC"
    planned_numbers = None
    if plan_rel in paths:
        plan = yaml.safe_load((root / plan_rel).read_text(encoding="utf-8"))
        manifest_path = book / "rag" / "manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
        expected_sha = (manifest.get("source") or {}).get("sha256")
        entries = plan.get("chapters", []) if isinstance(plan, dict) else []
        numbers = [c.get("number") for c in entries if isinstance(c, dict)]
        valid = (
            isinstance(plan, dict)
            and plan.get("schema") == "biblioteka-vsp/chapter-plan/v1"
            and plan.get("book_id") == book_id
            and isinstance(expected_sha, str)
            and bool(SHA_RE.fullmatch(expected_sha))
            and plan.get("source_sha256") == expected_sha
            and isinstance(entries, list) and len(entries) > 0
            and len(numbers) == len(entries)
            and all(isinstance(n, int) and not isinstance(n, bool) and n > 0 for n in numbers)
            and len(set(numbers)) == len(numbers)
            and all(
                isinstance(c.get("title"), str) and c["title"].strip()
                and c["title"] != "[Needs confirmation]"
                and isinstance(c.get("slug"), str) and c["slug"].strip()
                and isinstance(c.get("source_locator"), str) and c["source_locator"].strip()
                for c in entries
            )
            and isinstance(plan.get("toc_evidence"), str) and plan["toc_evidence"].strip()
            and plan.get("total_chapters") == len(entries)
        )
        if valid:
            total = len(entries)
            planned_numbers = set(numbers)
            toc_evidence = plan["toc_evidence"]
            reason = None
        else:
            reason = "Committed plan is invalid or its source SHA does not match the RAG manifest"

    published = sorted(complete if planned_numbers is None else complete & planned_numbers)
    missing = sorted(planned_numbers - set(published)) if planned_numbers is not None else None
    # No fractional progress if chapter total is unverified.
    percentage = round(len(published) * 100 / total, 1) if total is not None else None
    head = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    branch = subprocess.check_output(
        ["git", "-C", str(root), "branch", "--show-current"], text=True
    ).strip() or "(detached HEAD)"
    return {
        "book_id": book_id,
        "branch": branch,
        "commit": head,
        "total_chapters": total,
        "toc_evidence": toc_evidence,
        "unknown_reason": reason,
        "git_published_chapters": len(published),
        "published_chapter_numbers": published,
        "partial_chapter_numbers": sorted(partial),
        "remaining_chapters": len(missing) if missing is not None else None,
        "next_unpublished_chapter": missing[0] if missing else None,
        "progress_percent": percentage,
        "basis": "individual files in Git HEAD, not uncommitted files or ZIPs",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--book-id", required=True)
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        progress = get_progress(Path(args.repo_root), args.book_id)
    except (OSError, ValueError, subprocess.CalledProcessError, yaml.YAMLError) as exc:
        parser.exit(2, f"CHAPTER_PROGRESS_ERROR: {exc}\n")
    if args.json:
        print(json.dumps(progress, ensure_ascii=False, indent=2))
    else:
        total = progress["total_chapters"]
        shown_total = str(total) if total is not None else "[Needs confirmation]"
        ratio = f'{progress["git_published_chapters"]}/{total} ({progress["progress_percent"]}%)' if total is not None else f'{progress["git_published_chapters"]}/?'
        print(f'Книга: {args.book_id}; всего глав: {shown_total}; опубликовано в Git: {ratio}')
        print(f'Ветка: {progress["branch"]}; commit: {progress["commit"]}')
        if progress["unknown_reason"]:
            print(f'Причина неизвестного общего числа глав: {progress["unknown_reason"]}')
        else:
            print(f'Осталось: {progress["remaining_chapters"]}; следующая глава: {progress["next_unpublished_chapter"]}')
        print(f'Опубликованные главы: {progress["published_chapter_numbers"]}')
        if progress["partial_chapter_numbers"]:
            print(f'Не завершены в Git: {progress["partial_chapter_numbers"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
