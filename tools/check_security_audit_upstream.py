#!/usr/bin/env python3
"""Verify the Cloudflare snapshot; optionally perform a read-only upstream check.

Spec: knowledge/operations/cloudflare-security-audit.md
No installation, target audit, GitHub issue creation or upstream update is performed.
"""

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "vendor/cloudflare-security-audit-skill.lock.json"
VENDOR = ROOT / "vendor/cloudflare-security-audit-skill"


def verify_snapshot(lock, directory):
    """Require exactly the pinned regular files, with no symlink components."""
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("Vendor root is not a regular directory")
    expected = set()
    for entry in lock["files"]:
        name = entry["path"]
        if (not isinstance(name, str) or not name or name.startswith("/")
                or any(part in {"", ".", ".."} for part in name.split("/"))
                or "\\" in name or name in expected):
            raise ValueError("Invalid or duplicated manifest path")
        path = PurePosixPath(name)
        expected.add(name)
        target = directory
        for part in path.parts:
            target = target / part
            if target.is_symlink():
                raise ValueError("Symlink in vendor snapshot")
        if not target.is_file() or target.stat().st_size != entry["bytes"]:
            raise ValueError("Missing or resized vendor file: " + name)
        data = target.read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if hashlib.sha256(data).hexdigest() != entry["sha256"] or git_blob != entry["git_blob_sha1"]:
            raise ValueError("Changed vendor file: " + name)
    actual = set()
    for target in directory.rglob("*"):
        if target.is_symlink():
            raise ValueError("Unexpected vendor symlink")
        if target.is_file():
            actual.add(target.relative_to(directory).as_posix())
        elif not target.is_dir():
            raise ValueError("Unexpected special file")
    if actual != expected:
        raise ValueError("Vendor inventory differs from manifest")
    return len(expected)


def github_json(endpoint):
    result = subprocess.run(["gh", "api", endpoint], capture_output=True, text=True,
                            timeout=30, check=True)
    return json.loads(result.stdout)


def inspect(lock, now=None):
    """Compare the pin with upstream metadata; the lock date is provenance, not check history."""
    now = now or dt.datetime.now(dt.timezone.utc)
    files_verified = verify_snapshot(lock, VENDOR)
    # Fixed repository identity: the lock file cannot redirect authenticated requests elsewhere.
    if lock["repository"] != "https://github.com/cloudflare/security-audit-skill":
        raise ValueError("Unexpected upstream repository")
    metadata = github_json("repos/cloudflare/security-audit-skill")
    branch = metadata["default_branch"]
    if not re.fullmatch(r"[A-Za-z0-9._/-]{1,200}", branch) or ".." in branch:
        raise ValueError("Unexpected upstream branch")
    from urllib.parse import quote
    head = github_json("repos/cloudflare/security-audit-skill/commits/" + quote(branch, safe=""))
    releases = github_json("repos/cloudflare/security-audit-skill/releases?per_page=10")
    if not re.fullmatch(r"[0-9a-f]{40}", head["sha"]) or not isinstance(releases, list):
        raise ValueError("Unexpected GitHub response")
    stable = [r for r in releases if not r["draft"] and not r["prerelease"]]
    return {"schema_version": 2, "repository": lock["repository"], "pinned_commit": lock["commit"],
            "status": "current" if head["sha"] == lock["commit"] else "update_available",
            "files_verified": files_verified, "network_checked": True,
            "upstream_commit": head["sha"], "upstream_default_branch": branch,
            "latest_release": stable[0]["tag_name"] if stable else None,
            "checked_at": now.isoformat(), "next_check_due": (now + dt.timedelta(days=7)).isoformat()}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--remote", action="store_true", help="Read GitHub metadata via gh; never update files")
    mode.add_argument("--integrity-only", action="store_true",
                      help="Verify pinned local bytes; do not assess upstream freshness (default)")
    args = parser.parse_args()
    try:
        lock = json.loads(LOCK.read_text())
        if args.remote:
            report = inspect(lock)
        else:
            report = {"status": "integrity_verified", "files_verified": verify_snapshot(lock, VENDOR),
                      "network_checked": False, "upstream_freshness": "not_checked"}
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        # Do not print command stderr, environment or authenticated request material.
        print(json.dumps({"status": "unknown", "error_type": type(error).__name__}))
        return 3
    print(json.dumps(report, indent=2))
    return {"integrity_verified": 0, "current": 0, "update_available": 2}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())
