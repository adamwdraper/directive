# Impact Analysis — Cursor Project Rule and Combined Init Prompt

## Modules/packages likely touched
- `src/directive/cli.py` (init command: add combined prompt and scaffolding logic)
- Packaged resources under `src/directive/data/directive/cursor/**` (new)

## Contracts to update (APIs, events, schemas, migrations)
- CLI interface: `directive init` gains one combined yes/no question (default yes)
  - “Add recommended Cursor setup (MCP server config + Project Rule)? (Y/n)”

## Risks
- Security:
  - Ensure no secrets are written; MCP config should not embed credentials.
- Performance/Availability:
  - None; local one-time init.
- Data integrity:
  - Must be non-destructive: if files exist, skip and log a clear message.

## Additional Notes
- Implementation should copy pre-authored templates from packaged data (`directive/data/directive/cursor/**`) to `.cursor/` instead of writing hardcoded strings.
- Prefer idempotent operations so running `directive init` multiple times is safe.
