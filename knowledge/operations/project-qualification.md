---
type: Runbook
title: "Project coverage and runtime qualification"
description: "Choose a small project profile, expose coverage gaps and qualify the actual execution boundary."
status: draft
---

# Qualify a project, not a list of extensions

OPS separates three questions:

| Question | Evidence needed | Current repository capability |
| --- | --- | --- |
| Are the retained audit tools unchanged? | Full file inventory and hashes | Local checker; 22 pinned files |
| Was the project's source reviewed adequately? | Source revision, reviewed paths, applicable boundaries, checks and unresolved areas | Optional Cloudflare workflow and coverage ledger; no project audit is run automatically |
| Is execution constrained? | Tests of effective policy on an exact runtime/platform/harness/auth tuple | 16-control contract; no qualified runtime profile yet |

A successful integrity check answers only the first question. A valid findings file or a clean
scanner result cannot answer the other two by itself.

## Start with one project profile

Record the following in the project's existing task or qualification record; no new service or
OPS-specific configuration format is required:

1. Source revision, scope and material entry points: HTTP/API, CLI, file parsers, dependency setup,
   CI, credentials, MCP/tools, artifact export and deployment as applicable.
2. Tracked source, extensionless scripts, generated/vendor inputs, manifests and configuration.
   State exclusions and why. Inspect names, shebangs and build configuration; suffixes alone
   neither identify every executable nor establish coverage.
3. Native build/type/test commands and available dependencies. Run target-controlled setup and
   tests only inside the accepted execution boundary, not on the host during reconnaissance.
4. Selected security checks, exact tool/rule versions and recognized files/manifests. Unsupported
   languages, parsing failures, ignored paths and missing dependency data remain visible.
5. Required OPS controls, enforcement owners and checks, with `pass`, `fail`, `unknown` or justified
   `not_applicable`. Unknown or failed required controls refuse launch; exceptions are not passes.

Use the project's compiler/tests for correctness. Select security tools for the project's actual
stack instead of installing every scanner:

| Project surface | Useful evidence to select | Common gap to retain |
| --- | --- | --- |
| Python scripts or services | Native tests/type checks; applicable SAST rules | Dynamic imports, subprocesses and framework behavior |
| TypeScript/JavaScript, including TSX | Native compiler/test/build checks; relevant web and SAST rules | Runtime data flows, dependencies and generated assets |
| Shell, Dockerfile, CI and extensionless launchers | Interpreter/configuration review; command and permission tracing | Executable paths missed by a suffix filter |
| Dependencies and images | Recognized lockfiles/manifests; version/digest and advisory evidence | Unsupported manifests, unresolved or vendored versions |
| Media, binary or uploaded files | Parser/upload/export boundary review and bounded fixtures | No meaningful source scan of the asset itself |

For example, [Semgrep CE](https://docs.semgrep.dev/semgrep-ce-languages),
[CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning)
and [OSV-Scanner](https://google.github.io/osv-scanner/supported-languages-and-lockfiles/) have
different language, analysis and manifest support. Consult the version actually selected.
None is installed or invoked by this guide. Do not infer universal support from a product name.

## Keep source-audit gaps in the existing ledger

For a Cloudflare audit, follow the retained [skill](../../vendor/cloudflare-security-audit-skill/skills/security-audit/SKILL.md)
and [reconnaissance instructions](../../vendor/cloudflare-security-audit-skill/skills/security-audit/RECONNAISSANCE.md).
Reuse its `coverage-ledger.json`; do not introduce a competing coverage schema. Its units relate
entry surfaces, trust boundaries, subsystems and attack classes to reviewed paths and evidence.
Companion selection follows the boundary discovered, not merely the language name.

Keep `blocked`, `deferred` and `out_of_scope` units visible. Quick or scoped runs report partial
coverage. Revalidate changed source and prior unresolved work. More agents or a count of scanned
extensions cannot close a missing boundary. Read the [integration runbook](cloudflare-security-audit.md)
before invoking an audit.

## Runtime support remains unqualified

| Candidate | Authentication | OPS status |
| --- | --- | --- |
| OpenShell v0.1.5 with a declared Docker host/image and Claude Code version | User's Claude subscription token | Planned; compatibility, token isolation, revocation and lifecycle untested |
| Same runtime/platform/harness tuple | OpenRouter | Planned; protocol, provider, key mediation, usage and lifecycle untested |
| Docker Sandboxes, Modal or another runtime | Any | Comparison candidates; no OPS-qualified profile |

The first two rows do not establish that the upstream example profiles support these exact
combinations. Keep the [existing implementation sequence and acceptance checks](../components/agentic-ops.md#planned-implementation-sequence).
Record platform/kernel, runtime/harness versions, image/policy digests, check results and evidence
for each actual tuple. A readable real token cannot pass OPS-06 credential isolation.

Factory owns the development method; OPS owns execution qualification. SpaceShip owns admission
and delivery decisions, Observability owns measurement, and CROA assesses evidence. No module's
documentation, score or schema validator grants another module's authority.
