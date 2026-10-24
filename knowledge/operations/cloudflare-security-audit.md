---
type: Runbook
title: "Cloudflare security-audit integration and weekly maintenance"
description: "Complete pinned upstream snapshot, audit execution boundary, findings intake and mandatory checks at least every seven days."
status: draft
sources:
  - id: checker
    resource: ../../tools/check_security_audit_upstream.py
    title: "Read-only snapshot and freshness checker"
  - id: lock
    resource: ../../vendor/cloudflare-security-audit-skill.lock.json
    title: "Exact upstream inventory and hashes"
  - id: upstream
    resource: https://github.com/cloudflare/security-audit-skill
    title: "Cloudflare upstream and MIT license"
---

# Cloudflare security-audit

The complete repository snapshot at `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`
is retained unchanged under `vendor/cloudflare-security-audit-skill/`: **22 files**, including
the README, MIT license, skill, all companion documents, JSON schema, both validators and
their tests. The adjacent lock records every file's SHA-256 and Git blob identity. `.git`
transport metadata is not part of this source snapshot. Credit belongs to Cloudflare and
the upstream contributors. Æion neither authors nor certifies that skill.

## Role in OPS and SpaceShip

Use it as an optional source-audit workload. Read its original
[entry point](../../vendor/cloudflare-security-audit-skill/skills/security-audit/SKILL.md)
before invoking it. Merely adding it does not start an audit or authorize target execution.
Do not install it globally or grant all its agents broad host permissions.

Its structured findings distinguish established defects from unresolved leads. SpaceShip's
trusted intake must validate the records and source revision; schema validity cannot establish
that a vulnerability exists. An LLM finding cannot approve a merge, grant a capability or
mark an OPS control passed. Confidential findings go to private intake rather than public issues.

For a full audit, preserve upstream's complete workflow and independent verification. Run
target-controlled builds/tests only under its specified OS-enforced boundary: no external
network, sanitized allowlisted environment, read-only inputs, assigned scratch writes and
CPU/memory/process/disk/output/time limits. If that boundary is unavailable, retain the
validation blocker. An ordinary agent CLI allowlist is insufficient.

Use an explicit audit invocation budget and reserve verification effort before hunting.
Multiple correlated model opinions are not independent runtime evidence. Keep partial
coverage and `incomplete` status visible; a clean report is not a security certification.

## Mandatory weekly upstream check

**An operator must check upstream at least once every seven days**, even when GitHub publishes
no formal release. Check the default branch commit, recent releases/tags, changelog or README
changes, licence changes, and available security advisories. A release-only watcher can miss
new companion files and validator fixes. Urgent security notices trigger an earlier check.

The owner is the installation's security maintainer. SpaceShip's proposed `security-upstream`
routine owns scheduling after implementation; no scheduler has been installed by this document.
Store successful check time, observed branch/commit/release, checker version, status and next
deadline in the installation's protected maintenance journal. An offline integrity check or
failed network request does **not** renew that timestamp. A missed deadline raises a maintenance
ticket and blocks promotion of a *new* audit profile until reviewed; do not stop unrelated
production services solely because a research check is overdue.

```sh
python3 tools/check_security_audit_upstream.py --integrity-only
python3 tools/check_security_audit_upstream.py
python3 tools/check_security_audit_upstream.py --remote
```

`--integrity-only` verifies pinned bytes without checking freshness; it returns `integrity_verified`
and never renews the weekly check. The default checks local inventory and recorded age.
`--remote` uses authenticated `gh` only
for read-only public metadata. Neither prints credentials nor executes upstream code. Exit
`0` means integrity verified/current as labelled, `2` means update available, `3` means stale
or unknown/error. Its release field covers the first ten returned releases; review full
release/tag history separately when necessary. The checked default-branch SHA is the main
change detector. These are upstream checks, not supply-chain attestation or target auditing.

`current` means the checked default-branch commit matches the retained pin. The tool does not
review advisories, instruction changes or licences, and the local lock is not an independent
signature. The maintainer completes those review steps and records their scope separately.
For project/language coverage, use the [qualification guide](project-qualification.md); an
unchanged complete toolkit is not evidence that a target's whole source tree was audited.

Keep each remote JSON result as maintenance evidence. The source lock's original date remains
the snapshot provenance; a later successful check belongs in that journal, not an invented
new vendoring date. A network failure remains unknown and needs retry before the deadline.

## Updating safely

1. Create one deduplicated maintenance proposal for the old and new commits. Include changed
   paths, additions/removals, licence/notice changes, schema/validator compatibility and risk.
2. Stage the full new source tree in quarantine. Verify regular paths, expected upstream Git
   blobs and a fresh complete SHA-256 manifest. Preserve the upstream licence and notices.
3. Review skill instructions, execution requirements and validator code. No floating `main`,
   automatic `npx`, global installation or silent executable update in a running workload.
4. Run validator tests with a reviewed offline toolchain in a bounded disposable sandbox.
   Then replay representative confirmed, unresolved, rejected and incomplete audit fixtures.
5. A maintainer reviews the concrete diff. Publish a new pinned profile and keep the last
   compatible pin for rollback. Existing runs retain their frozen skill/schema versions.
6. Record the promotion and next check deadline. A newly added file must appear in the inventory;
   updating only SKILL.md is incomplete.

## Qualification status

The copy and hashes are present. See `work/cloudflare-validation.md` for actual checks executed.
This does not qualify an audit runtime, run a full codebase audit, or implement the weekly
scheduler. OPS remains a framework proposal pending its runtime acceptance checks.
