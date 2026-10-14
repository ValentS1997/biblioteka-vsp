#!/usr/bin/env python3
"""Validate published chapter/part study notes, Markdown links and SVG rendering.

This checks file-level integrity and rendering only; it does not verify that
chapter claims are scientifically true or that the RAG source PDF was read.
"""
from __future__ import annotations

import argparse
import re
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_RE = re.compile(r"(?<!!)\]\(([^)\n]+)\)")
SKIP = ("http://", "https://", "mailto:", "#", "data:")
CHAPTER_REQUIRED = (
    "README.md", "cheatsheet.md", "commands.md", "diagram.md",
    "visual-cheatsheet.svg", "visual-cheatsheet-detailed.svg"
)
FORBIDDEN_CHAPTER_ARCHIVE_EXTENSIONS = frozenset(
    {".zip", ".rar", ".7z", ".tar", ".tgz", ".gz", ".bz2", ".xz"}
)


def forbidden_chapter_archives(changed_paths: list[str]) -> list[str]:
    """Reject new archive substitutes anywhere in per-book notes.

    This runs against the *changed paths*, so historical unrelated notes stay
    backward-compatible while every new ZIP/archive chapter handoff fails CI.
    """
    offenders = []
    for raw in changed_paths:
        normalized = raw.replace("\\", "/")
        parts = normalized.split("/")
        if (len(parts) >= 4 and parts[0] == "books" and parts[2] == "notes"
                and Path(parts[-1]).suffix.lower() in FORBIDDEN_CHAPTER_ARCHIVE_EXTENSIONS):
            offenders.append(normalized)
    return sorted(set(offenders))



def check_svg(path: Path, out_dir: Path, issues: list[str]) -> None:
    try:
        raw = path.read_bytes()
        root = ET.fromstring(raw)
        if not root.tag.endswith("svg"):
            raise ValueError("not an SVG root")
        width = float(re.match(r"[\d.]+", root.attrib["width"]).group())
        height = float(re.match(r"[\d.]+", root.attrib["height"]).group())
        if width <= 10 or height <= 10:
            raise ValueError("invalid dimensions")
        if "viewBox" not in root.attrib:
            raise ValueError("missing viewBox")
        import cairosvg
        target = out_dir / (path.parent.name + "-" + path.name + ".png")
        cairosvg.svg2png(bytestring=raw, write_to=str(target))
        png = target.read_bytes()
        if png[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError("renderer did not produce PNG")
        rendered_w, rendered_h = struct.unpack(">II", png[16:24])
        if rendered_w < 100 or rendered_h < 100:
            raise ValueError("rendered PNG unexpectedly small")
    except Exception as exc:
        issues.append(f"{path}: SVG parse/render error: {exc}")


def check_markdown(path: Path, repo_root: Path, issues: list[str]) -> int:
    try:
        source = path.read_text(encoding="utf-8")
    except Exception as exc:
        issues.append(f"{path}: {exc}")
        return 0
    count = 0
    for raw_target in LINK_RE.findall(source):
        link = raw_target.strip().split(' "', 1)[0].strip("<>")
        if link.startswith(SKIP) or link.startswith("javascript:"):
            continue
        link = unquote(urlsplit(link).path)
        if not link:
            continue
        target = (path.parent / link).resolve()
        try:
            target.relative_to(repo_root)
        except ValueError:
            issues.append(f"{path}: relative link escapes repo: {raw_target}")
            continue
        if not target.is_file():
            issues.append(f"{path}: broken local link: {raw_target}")
        else:
            count += 1
    return count


def validate(book: Path) -> int:
    book = book.resolve()
    repo_root = Path(__file__).resolve().parent.parent
    if not book.is_dir() or not book.is_relative_to(repo_root):
        raise SystemExit("Invalid book directory")
    notes = book / "notes"
    chapters = sorted((notes / "chapters").glob("chapter-*"))
    if not chapters:
        raise SystemExit("No chapter directories found")
    issues: list[str] = []
    for folder in chapters:
        for name in CHAPTER_REQUIRED:
            if not (folder / name).is_file():
                issues.append(f"{folder}: missing required artifact {name}")
    svg_files = sorted(notes.rglob("*.svg"))
    md_files = sorted(notes.rglob("*.md"))
    count = 0
    with tempfile.TemporaryDirectory(prefix="chapter-svg-") as temp:
        for svg in svg_files:
            check_svg(svg, Path(temp), issues)
        for md in md_files:
            count += check_markdown(md, repo_root, issues)
    print(
        f"book={book.name}, chapter_dirs={len(chapters)}, markdown={len(md_files)}, "
        f"svg={len(svg_files)}, resolved_local_links={count}, issues={len(issues)}"
    )
    for issue in issues:
        print("ERROR:", issue)
    return 1 if issues else 0


def discover_books_with_chapters(repo_root: Path) -> list[Path]:
    """Discover only books that actually contain chapter note directories."""
    books_root = repo_root / "books"
    if not books_root.is_dir():
        return []
    return sorted(
        book for book in books_root.iterdir()
        if book.is_dir()
        and (book / "notes" / "chapters").is_dir()
        and any(p.is_dir() for p in (book / "notes" / "chapters").glob("chapter-*"))
    )


def validate_all_books(repo_root: Path) -> int:
    """Validate every book with chapter notes; fail if none or any fails."""
    books = discover_books_with_chapters(repo_root)
    if not books:
        print("ERROR: no books with chapter notes found", file=sys.stderr)
        return 1
    failed = 0
    for book in books:
        print(f"Validating chapter notes for {book.name}", flush=True)
        failed += bool(validate(book))
    print(f"Validated {len(books)} book(s); failed={failed}")
    return 1 if failed else 0



def select_changed_books(
    repo_root: Path, changed_paths: list[str], fallback_book: Path
) -> list[Path]:
    """Validate every chapter book touched in a PR/push; keep prior CI baseline.

    Legacy collections unrelated to a change are not automatically migrated.
    An opt-in --all-books command remains available for repository-wide audits.
    """
    active = {book.name: book for book in discover_books_with_chapters(repo_root)}
    selected: set[str] = set()
    for path in changed_paths:
        parts = path.replace("\\", "/").split("/")
        if len(parts) >= 4 and parts[0] == "books" and parts[2] == "notes":
            if parts[1] in active:
                selected.add(parts[1])
    if selected:
        return [active[name] for name in sorted(selected)]
    return [(repo_root / fallback_book).resolve()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--book-dir", help="validate one book (backward compatible)")
    group.add_argument("--all-books", action="store_true",
                       help="audit all books (including legacy collections)")
    group.add_argument("--changed-paths-file",
                       help="Git diff path list; validate every touched book with chapters")
    parser.add_argument("--fallback-book-dir",
                        default="books/computer-networks-olifer-7e-ru-2026")
    args = parser.parse_args()
    if args.all_books:
        sys.exit(validate_all_books(Path(__file__).resolve().parent.parent))
    if args.changed_paths_file:
        repo_root = Path(__file__).resolve().parent.parent
        changed = Path(args.changed_paths_file).read_text(encoding="utf-8").splitlines()
        archives = forbidden_chapter_archives(changed)
        if archives:
            for path in archives:
                print(f"ERROR: chapter notes archive is forbidden; publish individual Git files: {path}", file=sys.stderr)
            sys.exit(1)
        books = select_changed_books(repo_root, changed, Path(args.fallback_book_dir))
        return_code = 0
        for book in books:
            print(f"Validating chapter notes for {book.name}", flush=True)
            return_code |= validate(book)
        sys.exit(return_code)
    sys.exit(validate(Path(args.book_dir)))
