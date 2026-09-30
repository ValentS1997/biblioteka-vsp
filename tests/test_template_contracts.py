#!/usr/bin/env python3
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class TemplateContractTests(unittest.TestCase):
    def assert_template(self, path_name, template_id, version):
        path = TEMPLATES / path_name
        self.assertTrue(path.is_file(), path_name)
        doc = load(path)
        template = doc.get("template") or {}
        self.assertEqual(template_id, template.get("id"))
        self.assertEqual(version, str(template.get("version")))
        self.assertEqual("ACCEPTED", template.get("status"))
        return doc

    def test_new_book_branch_bootstrap_contracts(self):
        doc = self.assert_template(
            "book-branch-bootstrap-v1.0.yaml",
            "BIBLIOTEKA-VSP-BOOK-BRANCH-BOOTSTRAP",
            "1.0",
        )
        contracts = doc["contracts"]

        expected = {
            "onboarding": (
                "BIBLIOTEKA-VSP-BOOK-ONBOARDING",
                "1.0",
                "templates/book-onboarding-v1.0.yaml",
            ),
            "readiness": (
                "BIBLIOTEKA-VSP-BOOK-READINESS",
                "1.0",
                "templates/book-readiness-v1.0.yaml",
            ),
            "chapter_request": (
                "BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST",
                "1.0",
                "templates/chapter-analysis-request-v1.0.yaml",
            ),
            "chapter_artifacts": (
                "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION",
                "1.4",
                "templates/chapter-artifact-collection-v1.4.yaml",
            ),
        }

        for key, (template_id, version, rel_path) in expected.items():
            ref = contracts[key]
            self.assertEqual(template_id, ref["id"])
            self.assertEqual(version, str(ref["version"]))
            self.assertEqual(rel_path, ref["path"])

            target = ROOT / rel_path
            self.assertTrue(target.is_file(), rel_path)
            target_doc = load(target)
            target_template = target_doc.get("template") or {}
            self.assertEqual(template_id, target_template.get("id"))
            self.assertEqual(version, str(target_template.get("version")))
            self.assertEqual("ACCEPTED", target_template.get("status"))

    def test_chapter_request_targets_current_contracts(self):
        doc = self.assert_template(
            "chapter-analysis-request-v1.0.yaml",
            "BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST",
            "1.0",
        )
        readiness = doc["contracts"]["readiness"]
        artifacts = doc["contracts"]["artifact_collection"]

        self.assertEqual("BIBLIOTEKA-VSP-BOOK-READINESS", readiness["id"])
        self.assertEqual("1.0", str(readiness["version"]))
        self.assertEqual("templates/book-readiness-v1.0.yaml", readiness["path"])

        self.assertEqual(
            "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION",
            artifacts["id"],
        )
        self.assertEqual("1.4", str(artifacts["version"]))
        self.assertEqual(
            "templates/chapter-artifact-collection-v1.4.yaml",
            artifacts["path"],
        )

    def test_legacy_v13_retained_and_v14_current(self):
        v13 = self.assert_template(
            "chapter-artifact-collection-v1.3.yaml",
            "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION",
            "1.3",
        )
        v14 = self.assert_template(
            "chapter-artifact-collection-v1.4.yaml",
            "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION",
            "1.4",
        )
        self.assertNotIn("preconditions", v13["artifact_collection"])
        self.assertTrue(v14["artifact_collection"]["preconditions"]["book_level"]["chapter_analysis_ready"])


if __name__ == "__main__":
    unittest.main()
