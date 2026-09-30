#!/usr/bin/env python3
import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "stage_source_vault", REPO / "scripts" / "stage_source_vault.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class SourceVaultStageTests(unittest.TestCase):
    def test_discovers_only_top_level_supported_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.pdf").write_bytes(b"a")
            (root / "b.EPUB").write_bytes(b"b")
            (root / "c.txt").write_text("c", encoding="utf-8")
            (root / "nested").mkdir()
            (root / "nested" / "d.pdf").write_bytes(b"d")

            found = module.discover_sources(root)
            self.assertEqual(["a.pdf", "b.EPUB"], [path.name for path in found])

    def test_manifest_is_content_addressed_and_noncanonical(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "Книга.pdf"
            source.write_bytes(b"example")
            records = module.make_records([source])

            self.assertEqual(1, len(records))
            record = records[0]
            self.assertTrue(record.vault_path.startswith("source-vault/objects/"))
            self.assertTrue(record.vault_path.endswith(".pdf"))

            rendered = module.render_manifest("source-vault/test", records)
            self.assertIn('canonical_source: false', rendered)
            self.assertIn('canonical_status: "NOT_PROMOTED"', rendered)
            self.assertIn('original_name: "Книга.pdf"', rendered)


if __name__ == "__main__":
    unittest.main()
