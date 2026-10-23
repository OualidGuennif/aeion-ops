"""Regression checks for local integrity and weekly freshness behavior."""

import datetime as dt
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
import io
import json


spec = importlib.util.spec_from_file_location("checker", Path(__file__).with_name("check_security_audit_upstream.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        data = b"fixture\n"
        (self.root / "LICENSE").write_bytes(data)
        self.lock = {"checked_at": "2026-10-23", "repository": "https://github.com/cloudflare/security-audit-skill",
                     "commit": "a" * 40, "files": [{"path": "LICENSE", "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest(),
                     "git_blob_sha1": hashlib.sha1(b"blob 8\0" + data).hexdigest()}]}

    def test_complete_inventory(self):
        self.assertEqual(checker.verify_snapshot(self.lock, self.root), 1)

    def test_real_pinned_inventory(self):
        self.assertEqual(checker.verify_snapshot(json.loads(checker.LOCK.read_text()), checker.VENDOR), 22)

    def test_integrity_cli_does_not_claim_freshness_or_call_network(self):
        output = io.StringIO()
        with patch.object(checker, "LOCK") as lock, patch.object(checker, "VENDOR", self.root):
            lock.read_text.return_value = json.dumps(self.lock)
            with patch.object(checker, "github_json") as remote, patch.object(checker.sys, "argv", ["checker", "--integrity-only"]):
                with redirect_stdout(output):
                    result = checker.main()
        self.assertEqual(result, 0)
        self.assertEqual(json.loads(output.getvalue())["upstream_freshness"], "not_checked")
        remote.assert_not_called()

    def test_same_size_mutation(self):
        (self.root / "LICENSE").write_bytes(b"changed\n")
        with self.assertRaises(ValueError):
            checker.verify_snapshot(self.lock, self.root)

    def test_missing_file(self):
        (self.root / "LICENSE").unlink()
        with self.assertRaises(ValueError):
            checker.verify_snapshot(self.lock, self.root)

    def test_unexpected_file(self):
        (self.root / "extra").write_text("extra")
        with self.assertRaises(ValueError):
            checker.verify_snapshot(self.lock, self.root)

    def test_symlink(self):
        (self.root / "extra").symlink_to(self.root / "LICENSE")
        with self.assertRaises(ValueError):
            checker.verify_snapshot(self.lock, self.root)

    def test_duplicate_manifest_entry(self):
        self.lock["files"].append(dict(self.lock["files"][0]))
        with self.assertRaises(ValueError):
            checker.verify_snapshot(self.lock, self.root)

    def test_traversal_and_ambiguous_paths(self):
        for path in ["../LICENSE", "/LICENSE", "a//LICENSE", "a/./LICENSE", "a\\LICENSE"]:
            with self.subTest(path=path):
                self.lock["files"][0]["path"] = path
                with self.assertRaises(ValueError):
                    checker.verify_snapshot(self.lock, self.root)

    def test_weekly_boundary_and_offline_does_not_refresh(self):
        with patch.object(checker, "VENDOR", self.root):
            fresh = checker.inspect(self.lock, now=dt.datetime(2026, 10, 29, 23, 59, tzinfo=dt.timezone.utc))
            stale = checker.inspect(self.lock, now=dt.datetime(2026, 10, 30, tzinfo=dt.timezone.utc))
        self.assertFalse(fresh["weekly_check_due"])
        self.assertEqual(stale["status"], "stale")
        self.assertFalse(stale["network_checked"])

    def test_future_record_rejected(self):
        with patch.object(checker, "VENDOR", self.root):
            with self.assertRaises(ValueError):
                checker.inspect(self.lock, now=dt.datetime(2026, 10, 22, tzinfo=dt.timezone.utc))

    def test_remote_current_and_update(self):
        for commit, expected in [("a" * 40, "current"), ("b" * 40, "update_available")]:
            with self.subTest(commit=commit), patch.object(checker, "VENDOR", self.root):
                with patch.object(checker, "github_json", side_effect=[{"default_branch": "main"}, {"sha": commit}, []]):
                    result = checker.inspect(self.lock, remote=True)
            self.assertEqual(result["status"], expected)
            self.assertTrue(result["network_checked"])
            self.assertFalse(result["weekly_check_due"])

    def test_remote_error_is_not_a_successful_refresh(self):
        with patch.object(checker, "VENDOR", self.root), patch.object(checker, "github_json", side_effect=OSError):
            with self.assertRaises(OSError):
                checker.inspect(self.lock, remote=True)


if __name__ == "__main__":
    unittest.main()
