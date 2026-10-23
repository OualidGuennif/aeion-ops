---
type: Reference
title: "Agentic OPS research"
description: "Primary-source research on agent isolation, credentials, network enforcement, delivery, and observability, with explicit limits and proposed implications."
status: draft
sources:
  - id: factory
    resource: https://github.com/OualidGuennif/aeion-factory/tree/00fdbd0757b8ed3e08e71fa335de851234423c74
    title: "Factory public baseline"
  - id: openshell
    resource: https://github.com/NVIDIA/OpenShell/tree/v0.1.5
    title: "OpenShell stable source"
  - id: proposal
    resource: ../components/agentic-ops.md
    title: "Proposed framework"
---

# Research: operating coding agents safely

Checked: 2026-10-23. This is a curated synthesis of official documentation and public source,
not a copied collection of vendor documentation. Recommendations below are design proposals.
No runtime security experiments or paid inference calls were performed.

## Conclusion

Useful building blocks already exist. The opportunity for Æion is a small, teachable framework
that connects Factory to enforceable execution boundaries and reproducible checks. A new
container engine, model router, Kubernetes platform, or observability backend would add work
before demonstrating additional protection.

The core unit should be a control with an owner, an enforcement point, a negative test, an
evidence record, and a declared limitation. A checklist or prompt alone cannot establish that
an agent is confined. The proposed controls and release gates are in the
[framework proposal](../components/agentic-ops.md).

## Evidence and language

| Label | Meaning here |
| --- | --- |
| Source-verified | The cited documentation or source was read; behavior was not exercised |
| Locally verified | A command or test was run here, with its scope stated |
| Proposed | An Æion design choice requiring review and implementation |
| Unknown | Available evidence does not establish the behavior |

Security is conditional on the host, runtime, policy, credentials, workload, and version. No
profile should be described as perfectly secure. Passing tests covers those cases, not every
possible escape or prompt injection.

## Factory is the fixed foundation

The public Factory template was checked through GitHub: `OualidGuennif/aeion-factory`, MIT,
default branch `main`, commit `00fdbd0757b8ed3e08e71fa335de851234423c74`. Its instructions and
workflow already cover planning, specs, small branches, review, knowledge checks, and read-only
outer loops. The local Factory checkout was also inspected, but is on another branch and commit;
it should not silently become the public baseline. [F1]

OPS should reuse those conventions. Factory hooks guide behavior and catch errors; the operating
system, runtime, receiving service, and protected configuration must enforce permissions even
when the agent ignores repository instructions. CROA's definition and API remain unspecified.

## Runtime comparison

| Approach | What the sources establish | Recommended role and remaining work |
| --- | --- | --- |
| Ordinary Docker containers | Daemon access is sensitive; rootless mode reduces privilege; seccomp and user namespaces add controls. Containers still expose a shared kernel boundary. [D1–D4, G1] | Educational baseline for a single developer's selected repositories. Explicitly reject hostile multi-tenant claims. |
| NVIDIA OpenShell | Open-source policy and credential mediation with a supervisor outside the workload. Multiple compute runtimes are documented. [N1–N4] | First OSS integration candidate. Qualify the exact Docker-backed configuration before committing to it. |
| Docker Sandboxes | Local agent microVMs, proxy-managed credentials, and workspace modes are documented. [D5–D8] | Strong local comparator and possible optional integration. Verify distribution terms and exact controls before relying on it as an OSS dependency. |
| Modal Sandboxes | gVisor or VM isolation and explicit network controls are documented. [M1–M2] | Cloud reference and later optional integration. Current network and secret-injection combinations need careful validation. |
| gVisor / Firecracker directly | Additional syscall isolation or a KVM microVM foundation. [G1–G2] | Isolation building blocks, not complete agent operations frameworks. Avoid building a new infrastructure platform around them for v0. |

Ordinary Docker Desktop containers share its Linux VM; that is different from a separate VM per
agent. An isolated Git worktree also remains a host directory, not a sandbox. A Docker socket
mounted read-only still exposes an API; mount permissions do not make that API read-only. [D1, D4]

## OpenShell: useful, but qualify the actual configuration

GitHub identified `v0.1.5`, published 2026-10-20, as the stable release during research. Its
repository reports Apache-2.0. The documentation describes policy enforcement outside the
untrusted workload, and credentials replaced at authorized endpoints. [N1–N3]

The support matrix lists macOS Apple silicon with Docker Desktop and Linux support. It requires
Docker 28.0 for Docker-backed workflows and active kernel capability checks, including Landlock
ABI 3 and specific seccomp operations. A version string alone is insufficient. Unsupported
capabilities must cause preflight refusal rather than a less isolated launch. [N4]

Important defaults and gaps:

- L7 `audit` mode logs violations while forwarding traffic. An Æion enforcement profile must
  explicitly select and test `enforce`. [N5]
- `tls: skip` removes inspection and credential substitution. It cannot silently satisfy a
  control that requires either property. [N5]
- Native provider attachments authorize an endpoint; they do not choose or rewrite the model.
  Model selection and inference parameters remain client concerns. [N3]
- The versioned `claude-code` example accepts Anthropic API keys; it is not a ready-made
  subscription OAuth-token integration. Its telemetry destinations should also be reviewed. [N6]
- The `openrouter` example names the OpenCode binary and `OPENROUTER_API_KEY`. Claude Code uses
  a different binary and token-variable mapping, so importing that example unchanged is
  insufficient. [N7, A3]
- The trusted Docker controller needs daemon access. The untrusted workload must never receive
  that socket or the authority to edit its own effective policy. [N2, N4]

OpenShell already provides runtime signals, including OCSF security events and OTLP export.
That can supply trusted boundary evidence alongside agent-reported events. [N8]

## What to learn from Modal

Modal documents two isolation runtimes, gVisor and VMs, and prevents Sandboxes from automatically
accessing other Modal resources. This suggests a good rule: create a workload with only explicitly
attached capabilities. [M1]

However, outbound connections to public IPs are allowed by default. Its domain allowlist is beta,
and DNS remains unrestricted except under full network blocking. A domain list therefore does
not establish the absence of DNS exfiltration. [M1]

The beta secret-injection feature substitutes HTTPS headers outside the Sandbox. This is a useful
credential design, but its documented limitations currently prevent combining an Outbound Policy
with `block_network`, domain/CIDR allowlists, or memory snapshots. It also only supports HTTP/1.1
and does not cover sidecars. Do not publish an example claiming all of those protections operate
together. [M2]

For Æion, the lesson is to test the complete configuration, including DNS, sidecars, TLS clients,
and cleanup. Do not transfer a vendor's isolation claim to an arbitrary local Docker Compose setup.

## What to learn from Docker Sandboxes

Docker's local product provides a microVM boundary and host-side credential injection. Its
security documentation also identifies explicit host connections: workspace sharing, skills,
SSH-agent forwarding, and MCP. Local stdio MCP servers execute on the host, so a broad host MCP
can cross the intended isolation boundary. [D5]

Use a private clone or mountless workflow where possible. Disable unnecessary shared skills and
SSH-agent forwarding; review effective wildcard network rules. The documentation contains
different descriptions of the default skills mount, so inspect the effective mount instead of
relying on a default. [D5, D7]

OAuth passthrough deliberately exposes a real token to the guest; host-side masking and passthrough
must not receive the same credential-isolation status. Headless Linux can also fall back to a
permission-protected credential file instead of an OS keychain. [D8]

GitHub's stable release endpoint returned `v0.49.2` (2026-10-21), while the fetched release-notes
page headed with `0.49.1`. Use the release source and exact qualification results when selecting
a version, and refresh existing images as well as the CLI when an upstream advisory requires it.
The `sbx` CLI was not found on this machine's PATH. [D6, D9]

## Keep both authentication paths

| Path | Source-verified behavior | Framework implication |
| --- | --- | --- |
| Claude subscription token | `claude setup-token` produces a long-lived token used through `CLAUDE_CODE_OAUTH_TOKEN`; initial browser authorization is required. [A1–A2] | A container need not repeat browser login every run. Keep identity per user, protect the token, test expiry/revocation and container recreation. |
| OpenRouter | Claude Code can use the Anthropic-compatible endpoint `https://openrouter.ai/api` with `ANTHROPIC_AUTH_TOKEN`; conflicting API-key configuration needs handling. [A3] | Separate provider configuration from execution policy. Protect the key outside the workload where mediation is qualified. |
| DeepInfra, later | Both OpenAI-compatible and Anthropic-compatible endpoints are documented, including a Claude Code guide. [I1–I2] | Possible later provider integration; do not make it a third v0 implementation requirement. |

Claude's token documentation currently describes a one-year token and feature limitations,
including no Remote Control or claude.ai connectors. These are current vendor statements, not
an Æion guarantee of token lifetime or unlimited subscription capacity. [A1]

Passing a real token as an environment variable lets workload code read it. A Docker secret file
also remains readable to a process granted access. These techniques can improve handling but
do not establish credential non-disclosure. The stronger target is proxy-side substitution with
only an opaque value available to the workload. Qualification must prove that this works for
the subscription token as well as OpenRouter. [M2, D8, N3]

OpenRouter explicitly limits its Claude Code compatibility guarantee to Anthropic's first-party
provider. General multi-model availability does not prove identical tool use, streaming,
reasoning, context, or error behavior. Test a provider/model/harness combination before marking it
supported. [A3]

An OSS framework can document a separately installed Claude Code binary without claiming that
binary is OSS. Anthropic's current distribution guidance also matters if Æion later becomes a
hosted product; it requires end-user authentication and restricts modifying authentication.
That is a later product-design constraint, not a reason to remove either requested path. [A4]

## Observability and cost: contract first

Claude Code already exports OpenTelemetry metrics and events, with optional traces. Its cost
metrics are estimates, and its event stream does not expose every intermediate API retry.
Consequently, agent telemetry alone cannot establish billing truth or a complete security audit.
Raw prompts, bodies, tool arguments, and responses must remain disabled in the default profile.
[O1]

OpenTelemetry's GenAI conventions moved to a separate repository and remain in Development in
the source checked here. Pin the convention revision and keep Æion extensions namespaced rather
than assuming a permanently stable `gen_ai.*` schema. [O2–O3]

OpenRouter documents returned usage and cost, including the final SSE usage message, and says
old opt-in usage parameters are deprecated. This is evidence for its documented API response
format; do not assume the Anthropic-compatible Claude Code endpoint preserves every field.
Capture fixtures and reconcile with provider records. [R1]

Routing settings also matter. Providers can ignore unsupported parameters unless requirements
are enforced; routing and fallback can change the serving provider. Record requested versus
observed model/provider, and requested versus confirmed inference settings. Unknown effective
temperature, top-p, reasoning effort, or provider remains unknown. [R2]

Use provider-returned cost where available, reconcile later, and distinguish it from a locally
calculated estimate or a subscription allocation. Never count cached/reasoning subtotals twice,
and never convert missing usage to zero. Exact per-request subscription billing is not
established by these sources. Provider keys can have spend limits, but that alone does not prove
a strict zero-overshoot budget under concurrent in-flight requests. [R1, R3]

Privacy depends on the actual provider and settings. OpenRouter has routing controls for
retention; DeepInfra documents exceptions for particular upstream model providers. Neither an
aggregation API nor an environment variable is evidence of universal retention or residency
guarantees. A strict retention requirement may conflict with a selected compatible endpoint;
refuse or choose another explicit configuration. [R4–R5, I3]

## DevSecOps practices to carry over

Factory's branch and review workflow should be complemented by protected execution configuration,
short-lived and scoped credentials where supported, pinned build inputs, image and dependency
scanning, and evidence tied to the reviewed artifact. GitHub recommends minimum token
permissions and immutable action references, and warns about untrusted checkout and workflow
input. A source change must not be able to weaken its own release gate. [C1]

SLSA provides a vocabulary for artifact provenance; NIST SSDF provides lifecycle practices.
Use them as mappings for concrete controls, without claiming certification or a SLSA level just
because an SBOM or signature exists. [C2–C3]

OWASP's agent guidance covers tool misuse, identity, supply chain, context poisoning, and
agent-triggered actions. A malicious README, dependency install script, skill, or MCP response
must be assumed capable of influencing the model. Authorization and containment therefore need
to hold even when the model follows that content. [S1–S2]

The OpenAI documentation independently distinguishes sandbox boundaries from approval policy.
This supports keeping operator decisions and technical enforcement explicit in the framework;
permission prompts alone do not establish isolation. [O4]

## Source register

All links below were opened or retrieved during this research. Versioned source files were also
read through the GitHub API where noted. Short findings above are synthesis; source documentation
is not redistributed. IDs are local research references, not external standard control IDs.

| ID | Primary source | Evidence used |
| --- | --- | --- |
| F1 | [Factory baseline](https://github.com/OualidGuennif/aeion-factory/tree/00fdbd0757b8ed3e08e71fa335de851234423c74) | GitHub metadata and AGENTS.md retrieved; local workflow and checks inspected |
| N1 | [OpenShell v0.1.5](https://github.com/NVIDIA/OpenShell/releases/tag/v0.1.5) | Stable release metadata and repository license via GitHub API |
| N2 | [OpenShell architecture](https://docs.nvidia.com/openshell/latest/about/architecture) | Supervisor/workload trust boundary |
| N3 | [OpenShell inference](https://docs.nvidia.com/openshell/latest/how-it-works/inference) | Endpoint-bound substitution and native client ownership |
| N4 | [OpenShell support matrix](https://docs.nvidia.com/openshell/latest/about/support-matrix) | Also read docs/about/support-matrix.mdx at v0.1.5 via API |
| N5 | [OpenShell security controls](https://docs.nvidia.com/openshell/latest/security/best-practices) | Enforce versus audit; TLS inspection consequences |
| N6 | [Claude Code profile at v0.1.5](https://github.com/NVIDIA/OpenShell/blob/v0.1.5/providers/claude-code.yaml) | API-key variables, binaries, telemetry endpoints; API read |
| N7 | [OpenRouter profile at v0.1.5](https://github.com/NVIDIA/OpenShell/blob/v0.1.5/providers/openrouter.yaml) | OpenCode binary and bearer mapping; API read |
| N8 | [OpenShell observability](https://docs.nvidia.com/openshell/latest/observability) | OCSF, OTLP, runtime evidence |
| D1 | [Docker Engine security](https://docs.docker.com/engine/security/) | Daemon authority and execution boundary |
| D2 | [Docker rootless mode](https://docs.docker.com/engine/security/rootless/) | Non-root daemon/container operation |
| D3 | [Docker seccomp](https://docs.docker.com/engine/security/seccomp/) | Syscall filtering; preserve runtime compatibility |
| D4 | [OWASP Docker security](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html) | Socket exposure, capabilities, resource limits |
| D5 | [Docker Sandboxes security](https://docs.docker.com/ai/sandboxes/security/) | MicroVM, mounts, network, MCP and shared-resource caveats |
| D6 | [Docker Sandboxes release notes](https://docs.docker.com/ai/sandboxes/release-notes/) | CLI changes and security fixes; page/release drift |
| D7 | [Shared agent skills](https://docs.docker.com/ai/sandboxes/workflows/agent-skills/) | Read-only default described; compare effective configuration |
| D8 | [Docker credential handling](https://docs.docker.com/ai/sandboxes/configuration/credentials/) | Host-side injection, OAuth passthrough, Linux storage fallback |
| D9 | [Docker Sandboxes v0.49.2](https://github.com/docker/sbx-releases/releases/tag/v0.49.2) | Stable release endpoint and release body |
| G1 | [gVisor security model](https://gvisor.dev/docs/architecture_guide/security/) | Additional isolation, scope and residual threats |
| G2 | [Firecracker](https://firecracker-microvm.github.io/) | KVM microVM foundation; not a complete agent framework |
| M1 | [Modal networking and security](https://modal.com/docs/guide/sandbox-networking) | Isolation choices, public egress default, DNS limitation |
| M2 | [Modal secret injection](https://modal.com/docs/guide/sandbox-secret-injection) | Beta header substitution and incompatible controls |
| A1 | [Claude authentication](https://code.claude.com/docs/en/authentication) | setup-token, credential precedence, feature limits |
| A2 | [Claude CLI reference](https://code.claude.com/docs/en/cli-reference) | Non-interactive invocation and token command |
| A3 | [Claude Code on OpenRouter](https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration) | Native protocol, variables, compatibility caveat |
| A4 | [Claude legal and distribution guidance](https://code.claude.com/docs/en/legal-and-compliance) | Hosted-product conditions and unmodified authentication |
| I1 | [DeepInfra chat API](https://docs.deepinfra.com/chat/overview) | OpenAI-compatible endpoint |
| I2 | [DeepInfra Anthropic integration](https://docs.deepinfra.com/integrations/anthropic) | Messages endpoint and Claude Code integration |
| I3 | [DeepInfra privacy](https://docs.deepinfra.com/account/data-privacy) | Documented upstream exceptions and metadata |
| O1 | [Claude monitoring](https://code.claude.com/docs/en/monitoring-usage) | Native OTel, content gates, estimates, retry visibility |
| O2 | [OTel GenAI migration page](https://opentelemetry.io/docs/specs/semconv/gen-ai/) | Move to a separate repository |
| O3 | [OTel GenAI source](https://github.com/open-telemetry/semantic-conventions-genai/tree/9ffc7e00c639be7712e544e3e54331e885dccf84) | README and model spans retrieved; Development status |
| O4 | [OpenAI approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) | Approval policy versus technical sandbox boundary |
| R1 | [OpenRouter usage accounting](https://openrouter.ai/docs/cookbook/administration/usage-accounting) | Native usage, cost, streaming, deprecated flags |
| R2 | [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection) | Parameter requirements and provider selection |
| R3 | [OpenRouter agent key caps](https://openrouter.ai/docs/guides/best-practices/capping-shared-agent-keys) | Per-key limits and BYOK accounting settings |
| R4 | [OpenRouter data collection](https://openrouter.ai/docs/guides/privacy/data-collection) | Retention configuration |
| R5 | [OpenRouter ZDR](https://openrouter.ai/docs/guides/features/zdr) | Endpoint eligibility, upstream policy and routing constraints |
| C1 | [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Permissions, immutable actions, untrusted input/checkout |
| C2 | [SLSA 1.2](https://slsa.dev/spec/v1.2/) | Artifact and source provenance vocabulary |
| C3 | [NIST SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | Secure development lifecycle guidance |
| S1 | [OWASP Agentic Top 10](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) | Agent risk categories |
| S2 | [OWASP agent security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) | Tool, identity, context and validation practices |

## Remaining unknowns

1. Which exact local runtime/platform combination passes the required isolation probes.
2. Whether Claude subscription OAuth works with opaque credential substitution on that runtime.
3. Which provider usage fields survive the actual Claude Code/OpenRouter protocol path.
4. Which inference settings the selected harness can set and the serving endpoint can confirm.
5. End-to-end limits under concurrent requests, abrupt disconnects, and revocation.
6. GitHub visibility and approval to move from the requested planning phase to implementation.

These are implementation qualification tasks. No existing entry in this research is a claim
that Æion already implements or passes the corresponding control.
