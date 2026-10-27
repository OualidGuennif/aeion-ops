# Current work

## Checker freshness and vendor modes — COMPLETE (2026-10-27)
- Scope: the offline default mode judged freshness from the lock's provenance date, so it would report `stale` permanently after 2026-10-30 even with weekly remote checks; two validators were tracked `100644` although the lock pins `100755`.
- Result: the default mode is now integrity-only; `--remote` reports `checked_at`/`next_check_due` for the maintenance journal, which alone records freshness. Restored the pinned validator modes; contents unchanged.
- Validation: 13 checker tests passed on Python 3.9, 3.11, 3.12 and 3.13, including a new git-index mode check; 22 files verified. No remote check succeeded here (`gh` unavailable), so the existing weekly deadline still stands.

## Project coverage and research refresh — COMPLETE (2026-10-24)
- Scope: compare current runtime/security approaches with the existing Æion contracts, clarify language/project coverage, and simplify public adoption docs.
- Result: retained the 16 controls, checker and unchanged Cloudflare snapshot; added a project qualification guide and corrected stale Factory/CROA integration text.
- Validation: 13 checker tests and 65 upstream validator tests passed; all 22 retained files verified; read-only upstream check still matched the pin. See [validation](ops-review-validation.md).
- Next: qualify one exact OpenShell/platform/image/harness tuple, then the two authentication paths separately. No runtime, provider integration or automatic scanner was installed.

## Qualify Agentic OPS runtime — PLANNED
- Owner decision: 2026-10-23, keep Factory and both Claude subscription-token and OpenRouter options; focus on the framework and research first.
- State: runtime remains unimplemented; Cloudflare source-audit tooling is retained separately with explicit evidence and weekly maintenance instructions.
- Next: qualify the first runtime/authentication slice through SpaceShip's implementation gates; the independent public module is aeion-ops.
- Blocker: no runtime qualification or live credential test is claimed by this planning work.
- Evidence: knowledge/references/agentic-ops-research.md; public Factory commit 00fdbd0757b8ed3e08e71fa335de851234423c74.

## Cloudflare integration — COMPLETE
- Owner decision: 2026-10-23, retain all of cloudflare/security-audit-skill and document checks at least weekly.
- State: all 22 files preserved at c1c8a8c1471069fb0e188eeaff69b8e8db6564a8; hashes verified; 65 upstream tests and 13 checker tests passed; an integrity-only standalone command is available.
- Next: the installation's security maintainer repeats the upstream check no later than 2026-10-30; future SpaceShip scheduling remains planned.
- Blocker: no automatic scheduler, target audit or runtime enforcement qualification is installed.
- Evidence: knowledge/operations/cloudflare-security-audit.md; work/cloudflare-validation.md; vendor/cloudflare-security-audit-skill.lock.json.
