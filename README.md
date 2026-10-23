# Æion OPS

**Security and operations directives for coding agents — independently usable.**

Use OPS to define what an agent may read, write, call, spend and export. Apply the directives
to an existing workflow, or combine them with other Æion modules. No other Æion checkout is
required for the documentation or the local maintenance tool.

**Available:** the 16-control framework, source research, the complete pinned Cloudflare audit
skill and a tested integrity/upstream checker. **Planned:** a qualified sandbox, credential
mediation and live provider integrations. This repository does not currently enforce isolation.

Part of the modular [Æion SpaceShip framework](https://github.com/OualidGuennif/aeion-spaceship).
[Factory](https://github.com/OualidGuennif/aeion-factory) ·
[OPS](https://github.com/OualidGuennif/aeion-ops) ·
[CROA](https://github.com/OualidGuennif/aeion-croa) ·
[Observability](https://github.com/OualidGuennif/aeion-observability) ·
[SpaceShip](https://github.com/OualidGuennif/aeion-spaceship).
See the [module comparison and examples](https://github.com/OualidGuennif/aeion-spaceship/blob/main/docs/modules.md).

## Try the local tool

Python 3.9+ and the standard library are sufficient. No provider key, Docker or model call is needed:

```sh
git clone https://github.com/OualidGuennif/aeion-ops.git
cd aeion-ops
python3 tools/check_security_audit_upstream.py --integrity-only
```

Expected: `integrity_verified`, `files_verified: 22`, and `upstream_freshness: not_checked`.
This verifies the retained source bytes. It does not run an audit or establish sandbox security.

For the **at least weekly** read-only upstream check, install/configure `gh` as the operator and
run `python3 tools/check_security_audit_upstream.py --remote`. Exit `0` is current, `2` is a new
upstream commit, and `3` is unknown/error. No automatic updater or scheduler is installed.

## Apply the framework

1. Read the [execution contract](knowledge/components/agentic-ops.md) and choose your required controls.
2. Define task paths, allowed destinations, resource/deadline limits and credential handling.
3. Qualify the exact runtime/platform/harness/authentication combination against the checks.
4. Keep unsupported controls visible; do not treat a Docker configuration example as proof.

Both Claude subscription tokens and OpenRouter remain planned authentication paths. Their
credential-isolation and billing guarantees differ and need separate qualification. Factory is
the shared development method; you can also use these directives with your existing method.

## Read next

| Document | Purpose |
| --- | --- |
| [Framework](knowledge/components/agentic-ops.md) | Controls, boundaries and acceptance checks |
| [Research](knowledge/references/agentic-ops-research.md) | Primary sources, runtime comparisons and limitations |
| [Cloudflare integration](knowledge/operations/cloudflare-security-audit.md) | Complete snapshot, safe invocation and weekly maintenance |
| [Validation](work/cloudflare-validation.md) | Actual integrity and validator test evidence |
| [Credits](CREDITS.md) | Upstream attribution and preserved licence |

Original Æion material is [MIT](LICENSE). Vendored upstream content retains its own licence.
Research baseline: **2026-10-23**. Run local regression checks with
`python3 -m unittest discover -s tools -p 'test_*.py' -v`.
