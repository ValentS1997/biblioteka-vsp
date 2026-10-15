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
            "book-branch-bootstrap-v1.3.yaml",
            "BIBLIOTEKA-VSP-BOOK-BRANCH-BOOTSTRAP",
            "1.3",
        )
        expected = {
            "onboarding": ("BIBLIOTEKA-VSP-BOOK-ONBOARDING", "1.3", "templates/book-onboarding-v1.3.yaml"),
            "rag_ingestion_acceptance": ("BIBLIOTEKA-VSP-RAG-INGESTION-ACCEPTANCE", "1.0", "templates/rag-ingestion-acceptance-v1.0.yaml"),
            "readiness": ("BIBLIOTEKA-VSP-BOOK-READINESS", "1.3", "templates/book-readiness-v1.3.yaml"),
            "chapter_request": ("BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST", "1.3", "templates/chapter-analysis-request-v1.3.yaml"),
            "chapter_artifacts": ("BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION", "1.7", "templates/chapter-artifact-collection-v1.7.yaml"),
        }
        for key, (template_id, version, rel_path) in expected.items():
            ref = doc["contracts"][key]
            self.assertEqual(template_id, ref["id"])
            self.assertEqual(version, str(ref["version"]))
            self.assertEqual(rel_path, ref["path"])
            target_doc = load(ROOT / rel_path)
            target_template = target_doc.get("template") or {}
            self.assertEqual(template_id, target_template.get("id"))
            self.assertEqual(version, str(target_template.get("version")))
            self.assertEqual("ACCEPTED", target_template.get("status"))

    def test_chapter_request_targets_current_contracts(self):
        doc = self.assert_template(
            "chapter-analysis-request-v1.3.yaml",
            "BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST",
            "1.3",
        )
        readiness = doc["contracts"]["readiness"]
        artifacts = doc["contracts"]["artifact_collection"]
        self.assertEqual("1.3", str(readiness["version"]))
        self.assertEqual("templates/book-readiness-v1.3.yaml", readiness["path"])
        self.assertEqual("1.7", str(artifacts["version"]))
        self.assertEqual("templates/chapter-artifact-collection-v1.7.yaml", artifacts["path"])

    def test_legacy_versions_retained_and_v16_current(self):
        self.assert_template("book-onboarding-v1.1.yaml", "BIBLIOTEKA-VSP-BOOK-ONBOARDING", "1.1")
        self.assert_template("book-readiness-v1.1.yaml", "BIBLIOTEKA-VSP-BOOK-READINESS", "1.1")
        self.assert_template("chapter-artifact-collection-v1.5.yaml", "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION", "1.5")
        v16 = self.assert_template(
            "chapter-artifact-collection-v1.6.yaml",
            "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION",
            "1.6",
        )
        self.assertTrue(v16["artifact_collection"]["preconditions"]["book_level"]["chapter_analysis_ready"])
        self.assertIn("epub", v16["artifact_collection"]["source_policy"]["supported_source_formats"])

    def test_onboarding_supports_pdf_and_epub(self):
        onboarding = self.assert_template(
            "book-onboarding-v1.3.yaml",
            "BIBLIOTEKA-VSP-BOOK-ONBOARDING",
            "1.3",
        )
        formats = onboarding["policy"]["supported_canonical_source_formats"]
        self.assertEqual(["pdf", "epub"], formats)

    def test_process_compliance_router_targets_current_contracts(self):
        path = TEMPLATES / "process-compliance-router-v1.0.yaml"
        self.assertTrue(path.is_file(), path)
        doc = load(path)
        router = doc.get("router") or {}
        self.assertEqual("BIBLIOTEKA-VSP-PROCESS-COMPLIANCE-ROUTER", router.get("id"))
        self.assertEqual("1.0", str(router.get("version")))
        self.assertEqual("ACCEPTED", router.get("status"))
        self.assertTrue(doc["startup"]["mandatory"])
        self.assertTrue(doc["process_mode"]["fail_closed"])

        expected = {
            "book_branch_bootstrap": ("1.3", "templates/book-branch-bootstrap-v1.3.yaml"),
            "book_onboarding": ("1.3", "templates/book-onboarding-v1.3.yaml"),
            "rag_ingestion_acceptance": ("1.0", "templates/rag-ingestion-acceptance-v1.0.yaml"),
            "book_readiness": ("1.3", "templates/book-readiness-v1.3.yaml"),
            "chapter_analysis_request": ("1.3", "templates/chapter-analysis-request-v1.3.yaml"),
            "chapter_artifact_collection": ("1.7", "templates/chapter-artifact-collection-v1.7.yaml"),
            "git_execution": ("1.0", "templates/git-execution-policy-v1.0.yaml"),
        }
        for key, (version, rel_path) in expected.items():
            ref = doc["current_contracts"][key]
            self.assertEqual(version, str(ref["version"]))
            self.assertEqual(rel_path, ref["canonical_path"])
            target = load(ROOT / rel_path)
            self.assertEqual("ACCEPTED", (target.get("template") or {}).get("status"))

    def test_current_direct_git_chapter_publication_contracts(self):
        policy = self.assert_template(
            "chapter-publication-v1.0.yaml",
            "BIBLIOTEKA-VSP-CHAPTER-PUBLICATION", "1.0",
        )
        self.assertTrue(policy["startup"]["mandatory_on"])
        self.assertIn("zip", " ".join(policy["publication"]["forbidden_delivery"]).lower())
        self.assertFalse(policy["repository"]["direct_main_allowed"])
        self.assertEqual(6, len(policy["publication"]["required_individual_files"]))

        current = (
            ("book-branch-bootstrap-v1.4.yaml", "BIBLIOTEKA-VSP-BOOK-BRANCH-BOOTSTRAP", "1.4"),
            ("chapter-analysis-request-v1.4.yaml", "BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST", "1.4"),
            ("chapter-artifact-collection-v1.8.yaml", "BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION", "1.8"),
        )
        for path, template_id, version in current:
            doc = self.assert_template(path, template_id, version)
            ref = doc.get("contracts", {}).get("chapter_publication") or doc.get("artifact_collection", {}).get("chapter_publication_contract")
            self.assertEqual("templates/chapter-publication-v1.0.yaml", ref["path"])
        router = load(TEMPLATES / "process-compliance-router-v1.1.yaml")
        self.assertEqual("1.1", router["router"]["version"])
        expected = {
            "book_branch_bootstrap": ("1.4", "templates/book-branch-bootstrap-v1.4.yaml"),
            "chapter_analysis_request": ("1.4", "templates/chapter-analysis-request-v1.4.yaml"),
            "chapter_artifact_collection": ("1.8", "templates/chapter-artifact-collection-v1.8.yaml"),
            "chapter_publication": ("1.0", "templates/chapter-publication-v1.0.yaml"),
        }
        for key, (version, path) in expected.items():
            ref = router["current_contracts"][key]
            self.assertEqual(version, str(ref["version"]))
            self.assertEqual(path, ref["canonical_path"])
        self.assertTrue(router["routes"]["CHAPTER_ROUTE"]["publication"]["forbid_archive_substitute"])

    def test_session_recovery_router_is_current(self):
        recovery = self.assert_template(
            "session-recovery-v1.0.yaml",
            "BIBLIOTEKA-VSP-SESSION-RECOVERY", "1.0",
        )
        self.assertFalse(recovery["scope"]["no_background_execution"] is False)
        self.assertEqual(
            ".workflow/checkpoints/<task-key>.yaml",
            recovery["durable_checkpoint"]["location"],
        )
        self.assertFalse(recovery["durable_checkpoint"]["privacy"] is None)
        self.assertIn(
            "Ковальски, проверка после обрыва связи",
            recovery["recovery_trigger"]["exact_command"],
        )
        self.assertIn(
            "git", recovery["recovery_trigger"]["interrupted_operation_rule"].lower()
        )
        router = load(TEMPLATES / "process-compliance-router-v1.2.yaml")
        self.assertEqual("1.2", str(router["router"]["version"]))
        ref = router["current_contracts"]["session_recovery"]
        self.assertEqual("1.0", str(ref["version"]))
        self.assertEqual("templates/session-recovery-v1.0.yaml", ref["canonical_path"])
        self.assertTrue(router["routes"]["RECOVERY_ROUTE"]["no_duplicate_mutations"])
        self.assertTrue(router["compliance_checks"]["continuity"]["checkpoint_for_multi_step_work"])

    def test_remote_git_policy_is_current(self):
        policy = self.assert_template(
            "git-execution-policy-v1.0.yaml",
            "BIBLIOTEKA-VSP-GIT-EXECUTION-POLICY",
            "1.0",
        )
        self.assertFalse(policy["local_git_exception_policy"]["default_allowed"])


if __name__ == "__main__":
    unittest.main()
