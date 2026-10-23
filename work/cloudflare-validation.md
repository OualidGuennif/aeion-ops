# Cloudflare integration validation — 2026-10-23

Scope: retained source and maintenance tooling. No full target audit, global installation,
provider call or runtime-boundary qualification was performed.

- Complete upstream tree at `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`: **22 files,
  322,698 bytes**. Every retrieved Git blob identity and SHA-256 matched. Original MIT licence retained.
- Local checker: `python3 tools/check_security_audit_upstream.py` passed, exact inventory verified.
- Read-only remote check: **current** at `2026-10-23T09:01:53.234824+00:00`; default branch `main`
  still pointed at the pin; no stable release appeared in the queried ten-release page.
- Checker regression suite: **11 tests passed**, including changed/missing/extra files, symlink,
  duplicate/traversal paths, weekly expiry, future date, remote change and remote failure.
- Upstream Node validator suites: **65 tests passed, zero failed/skipped** in a disposable container.
  This establishes their test behavior, not correctness of findings or a secure target runtime.

The validator container used the already present Node image identity
`sha256:0a7108bf6c7bf5de370ffb1a3ed6be93d405b43ff159f681a8d18c0e2bc2e402`.
Network was disabled, root filesystem and vendor bind mount read-only, user `65534:65534`,
capabilities dropped, no-new-privileges, empty/allowlisted process environment, one CPU,
256 MiB memory/swap cap, 64 PIDs, 32 MiB scratch tmpfs, 8 MiB file cap and 60-second deadline.
No host home, secret store or Docker socket was mounted into the workload.

The first bounded test run passed 62/65 and failed three with `EFBIG`: a 1 MiB file cap prevented
intentional multi-megabyte fixtures from being written. Source inspection identified fixtures up
to the validator's 5 MiB input boundary. Raising only the declared bounded test envelope to the
values above allowed the unchanged upstream tests to pass. No upstream file was patched.

The seven-day remote-check deadline is **2026-10-30**. An operator must repeat the check and
retain its successful result; no weekly scheduler has been installed. See the
[maintenance runbook](../knowledge/operations/cloudflare-security-audit.md).
