#!/usr/bin/env python3
"""Stage future book sources into a dedicated Git LFS source-vault branch.

This is the single intended user-local Git exception for bulk preloading book
binaries. After the branch is pushed, normal biblioteka-vsp work returns to the
GitHub connector/API and repository automation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, NamedTuple

SUPPORTED_EXTENSIONS = {".pdf", ".epub"}
VAULT_ROOT = Path("source-vault")
OBJECTS_DIR = VAULT_ROOT / "objects"
MANIFEST_PATH = VAULT_ROOT / "manifest.yaml"


class StageError(RuntimeError):
    pass


class SourceRecord(NamedTuple):
    original_name: str
    extension: str
    sha256: str
    size_bytes: int
    vault_path: str


def run(
    *args: str,
    cwd: Path | None = None,
    check: bool = True,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        check=check,
        text=True,
        capture_output=capture,
    )


def repo_root() -> Path:
    result = run("git", "rev-parse", "--show-toplevel", capture=True)
    return Path(result.stdout.strip()).resolve()


def ensure_clean(repo: Path) -> None:
    result = run("git", "status", "--porcelain", cwd=repo, capture=True)
    if result.stdout.strip():
        raise StageError(
            "Working tree is not clean. Use a fresh clone or clean it before staging."
        )


def ensure_remote_branch_absent(repo: Path, branch: str) -> None:
    result = run(
        "git",
        "ls-remote",
        "--exit-code",
        "--heads",
        "origin",
        branch,
        cwd=repo,
        check=False,
        capture=True,
    )
    if result.returncode == 0:
        raise StageError(
            f"Remote branch {branch!r} already exists. Use a new immutable batch branch."
        )
    if result.returncode not in {2}:
        raise StageError(
            f"Could not check remote branch {branch!r}: exit {result.returncode}"
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def discover_sources(source_dir: Path) -> list[Path]:
    if not source_dir.is_dir():
        raise StageError(f"Source directory does not exist: {source_dir}")

    sources = sorted(
        (
            path
            for path in source_dir.iterdir()
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
        ),
        key=lambda path: path.name.casefold(),
    )
    if not sources:
        raise StageError(
            f"No top-level PDF/EPUB files found in {source_dir}"
        )
    return sources


def make_records(sources: Iterable[Path]) -> list[SourceRecord]:
    records: list[SourceRecord] = []
    for path in sources:
        digest = sha256_file(path)
        extension = path.suffix.lower()
        records.append(
            SourceRecord(
                original_name=path.name,
                extension=extension.removeprefix("."),
                sha256=digest,
                size_bytes=path.stat().st_size,
                vault_path=(OBJECTS_DIR / f"{digest}{extension}").as_posix(),
            )
        )
    return records


def yaml_quote(value: str) -> str:
    # JSON string syntax is valid YAML and robust for spaces/non-ASCII/punctuation.
    return json.dumps(value, ensure_ascii=False)


def render_manifest(branch: str, records: list[SourceRecord]) -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        'schema_version: "1.0"',
        "",
        "source_vault:",
        f"  branch: {yaml_quote(branch)}",
        f"  created_at_utc: {yaml_quote(now)}",
        '  storage: "Git LFS"',
        '  role: "pre-staged source candidates; not canonical book sources"',
        "  records:",
    ]

    for record in records:
        lines.extend(
            [
                f"    - original_name: {yaml_quote(record.original_name)}",
                f"      extension: {yaml_quote(record.extension)}",
                f"      sha256: {yaml_quote(record.sha256)}",
                f"      size_bytes: {record.size_bytes}",
                f"      vault_path: {yaml_quote(record.vault_path)}",
                '      book_id: "[Needs confirmation]"',
                '      canonical_status: "NOT_PROMOTED"',
            ]
        )

    lines.extend(
        [
            "",
            "policy:",
            '  canonical_source: false',
            '  registry_side_effects: false',
            '  rag_build_side_effects: false',
            '  promotion_required: true',
            '  promotion_target: "books/<book_id>/source/book.<ext>"',
            "",
        ]
    )
    return "\n".join(lines)


def stage_files(repo: Path, sources: list[Path], records: list[SourceRecord]) -> None:
    (repo / OBJECTS_DIR).mkdir(parents=True, exist_ok=True)

    by_name = {path.name: path for path in sources}
    for record in records:
        source = by_name[record.original_name]
        destination = repo / record.vault_path
        if destination.exists():
            if sha256_file(destination) != record.sha256:
                raise StageError(f"Content-addressed collision at {destination}")
            continue
        shutil.copy2(source, destination)

    (repo / MANIFEST_PATH).write_text(
        render_manifest(
            run("git", "branch", "--show-current", cwd=repo, capture=True).stdout.strip(),
            records,
        ),
        encoding="utf-8",
    )


def verify_lfs_tracking(repo: Path, records: list[SourceRecord]) -> None:
    for record in records:
        result = run(
            "git",
            "check-attr",
            "filter",
            "--",
            record.vault_path,
            cwd=repo,
            capture=True,
        )
        if "filter: lfs" not in result.stdout:
            raise StageError(
                f"Git LFS attribute missing for {record.vault_path}: {result.stdout.strip()}"
            )


def verify_staged_lfs(repo: Path, records: list[SourceRecord]) -> None:
    listed = run(
        "git",
        "lfs",
        "ls-files",
        "--name-only",
        cwd=repo,
        capture=True,
    ).stdout.splitlines()
    lfs_paths = set(listed)
    missing = [record.vault_path for record in records if record.vault_path not in lfs_paths]
    if missing:
        raise StageError(f"Files are not staged/tracked by Git LFS: {missing}")


def print_summary(branch: str, records: list[SourceRecord]) -> None:
    print("status: READY_TO_PUSH")
    print(f"branch: {yaml_quote(branch)}")
    print(f"source_count: {len(records)}")
    print("records:")
    for record in records:
        print(f"  - original_name: {yaml_quote(record.original_name)}")
        print(f"    sha256: {yaml_quote(record.sha256)}")
        print(f"    size_bytes: {record.size_bytes}")
        print(f"    vault_path: {yaml_quote(record.vault_path)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        required=True,
        help="Directory whose top-level PDF/EPUB files should be staged.",
    )
    parser.add_argument(
        "--branch",
        required=True,
        help="New immutable source-vault branch, e.g. source-vault/2026-09-30-rag-books.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Commit and push the source-vault branch after local verification.",
    )
    args = parser.parse_args()

    try:
        repo = repo_root()
        source_dir = Path(args.source_dir).expanduser().resolve()

        ensure_clean(repo)
        run("git", "lfs", "version", cwd=repo)
        run("git", "lfs", "install", "--local", cwd=repo)
        run("git", "fetch", "origin", "main", cwd=repo)
        ensure_remote_branch_absent(repo, args.branch)

        run("git", "switch", "--create", args.branch, "origin/main", cwd=repo)

        sources = discover_sources(source_dir)
        records = make_records(sources)
        stage_files(repo, sources, records)
        verify_lfs_tracking(repo, records)

        run("git", "add", "--", ".gitattributes", VAULT_ROOT.as_posix(), cwd=repo)
        verify_staged_lfs(repo, records)

        print_summary(args.branch, records)

        if not args.push:
            print("push_performed: false")
            print("next_action: rerun with --push after reviewing the staged manifest")
            return 0

        run(
            "git",
            "commit",
            "-m",
            f"chore(source-vault): stage {len(records)} book source(s)",
            cwd=repo,
        )
        run(
            "git",
            "push",
            "--set-upstream",
            "origin",
            f"HEAD:{args.branch}",
            cwd=repo,
        )

        remote = run(
            "git",
            "ls-remote",
            "--exit-code",
            "--heads",
            "origin",
            args.branch,
            cwd=repo,
            capture=True,
        )
        if not remote.stdout.strip():
            raise StageError("Remote branch verification returned no ref.")

        print("push_performed: true")
        print("remote_verification: PASS")
        print("next_action: delete the temporary clone if desired; future source promotion is remote")
        return 0

    except (StageError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
