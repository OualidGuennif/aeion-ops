# Æion OPS

**Define what a coding agent may access, execute and export.**

OPS is a security framework and a small maintenance toolkit for agent workflows. Use it on
its own, with your existing development method, or with [Æion Factory](https://github.com/OualidGuennif/aeion-factory).

- **16 controls** for files, network, credentials, resources, artifacts and cleanup.
- **A pinned Cloudflare security-audit toolkit**, including its instructions and validators.
- **A local checker** for toolkit integrity and read-only upstream change detection.

**Status:** the framework and maintenance tools are available. Runtime enforcement, credential
mediation and provider integrations still need implementation and qualification. Cloning OPS
does not isolate an agent or run a security audit.

## Try it

Python 3.9+; standard library only. No provider key or Docker needed:

```sh
git clone https://github.com/OualidGuennif/aeion-ops.git
cd aeion-ops
python3 tools/check_security_audit_upstream.py --integrity-only
```

Expected: `integrity_verified`, `files_verified: 22`, `upstream_freshness: not_checked`.
This verifies the bundled source bytes.

To check upstream at least weekly, configure GitHub CLI (`gh`) as the operator, then run
`python3 tools/check_security_audit_upstream.py --remote`. It reads metadata and never updates
the toolkit. Exit `0`: current; `2`: update available; `3`: unknown/error.
Follow the [maintenance runbook](knowledge/operations/cloudflare-security-audit.md) for review and evidence.

## Use it in a project

1. Choose the required [controls](knowledge/components/agentic-ops.md) and define allowed paths, destinations and limits.
2. Follow the [project qualification guide](knowledge/operations/project-qualification.md) to record checks and gaps.
3. Qualify the exact runtime, platform, harness and authentication path before relying on enforcement.

Controls apply across languages. Source-audit coverage depends on the actual files, frameworks
and trust boundaries reviewed. An unsupported or skipped area remains a visible gap.
Claude subscription tokens and OpenRouter are separate planned paths with separate qualification.

## Read next

- [Framework and implementation plan](knowledge/components/agentic-ops.md)
- [Research and primary sources](knowledge/references/agentic-ops-research.md)
- [Cloudflare integration](knowledge/operations/cloudflare-security-audit.md) · [validation evidence](work/cloudflare-validation.md)
- [Æion modules and responsibilities](https://github.com/OualidGuennif/aeion-spaceship/blob/main/docs/modules.md)

Run local regression checks: `python3 -m unittest discover -s tools -p 'test_*.py' -v`.
Original material: [MIT](LICENSE). Upstream material retains its own licence; see [credits](CREDITS.md).
