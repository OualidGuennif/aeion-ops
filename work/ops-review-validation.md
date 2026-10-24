# OPS project-coverage review — 2026-10-24

Scope: first-party documentation, current integration responsibilities and source research.
Production tooling, CI and the retained Cloudflare snapshot were left unchanged.

| Check | Observed result |
| --- | --- |
| `python3 tools/check_security_audit_upstream.py --integrity-only` | `integrity_verified`; 22 files; upstream freshness not checked by this mode |
| `python3 -m unittest discover -s tools -p 'test_*.py' -v` | 13 tests passed |
| Read-only `--remote` check | `current` at 2026-10-24T12:23:52.151614+00:00; branch `main` matched `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`; no release in the queried page |
| Both retained Node validator suites | 65 passed; zero failed, cancelled or skipped |
| First-party relative Markdown targets | Existing targets and the new implementation-plan anchor resolved |
| `git diff --check` | Passed |

Validator tests used the already present pinned image
`node@sha256:0a7108bf6c7bf5de370ffb1a3ed6be93d405b43ff159f681a8d18c0e2bc2e402`
with the [existing CI envelope](../.github/workflows/ci.yml): no network, read-only root and vendor
mount, UID/GID 65534, no capabilities, no-new-privileges, one CPU, 256 MiB memory/swap, 64 PIDs,
32 MiB scratch tmpfs, 8 MiB file cap and a 60-second independent command deadline. The host
supervisor removed the named container on completion. No target test code ran on the host.

The [new guide](../knowledge/operations/project-qualification.md) records the distinction between
tool integrity, project audit coverage and runtime qualification. The 16-control contract remains
a proposal. No runtime boundary, authentication path, model/provider compatibility, full project
security audit or deployed configuration was qualified by these checks.

The original source lock date remains snapshot provenance. This successful remote metadata check
has its own seven-day deadline of 2026-10-31T12:23:52.151614+00:00. Advisory/instruction/licence review
has its own scope; an installation maintainer must keep the complete maintenance journal. No
automatic scheduler or updater was installed.
