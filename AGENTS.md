# Working on Æion Agentic OPS

- Read README.md and knowledge/components/agentic-ops.md before meaningful changes.
- Factory remains the fixed method. Runtime controls are proposed until qualification proves them.
- Keep both Claude subscription-token and OpenRouter paths; report their distinct limitations.
- Keep code/docs/comments/logs in English and operator explanations in French.
- Never read or print credentials, ambient environments or authentication stores.
- Treat vendor/ as an immutable upstream snapshot. Update the whole tree and adjacent inventory
  only through reviewed promotion; preserve licences and credits.
- Adding the Cloudflare skill does not invoke a full audit or install it globally. Read its
  original instructions and the integration runbook before invoking it.
- Check upstream at least weekly; failed/offline checks cannot renew remote freshness.
- Do not execute target-controlled setup/tests on the host or claim Docker flags alone prove isolation.
- The maintenance checker verifies local files/read-only metadata; it is not a race-safe artifact
  importer, target scanner or runtime security boundary.
