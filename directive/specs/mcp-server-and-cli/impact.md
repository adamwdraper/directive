# Impact Analysis — MCP server and minimal CLI

## Modules/packages likely touched
- CLI package: console entry `directive` with subcommands `init`, `update`, `mcp serve`  
- MCP server package: resources and read-only bundle tool  
- Docs/templates: ship default templates as package data; copy to repo on init  

## Contracts to update (APIs, events, schemas, migrations)
- MCP Resources:  
  - `directive.files.list()` → list files under `directive/`  
  - `directive.file.get(path)` → return raw file content  
- MCP Tools (read-only):  
  - `spec.template()` → full AOP + Agent Context + `spec_template.md` + Primer  
  - `impact.template()` → full AOP + Agent Context + `impact_template.md` + Primer  
  - `tdr.template()` → full AOP + Agent Context + `tdr_template.md` + Primer  

## Risks
- Performance/Availability: responses include full AOP/Context/Template; acceptable for now but monitor large files.  
  - Mitigation: if files grow large later, consider streaming or chunked resources; for now, keep them small.  

## Observability needs
- Logs: tool invocations, target paths, refusal reasons (no secrets)  
- Metrics: count of tool calls, success/failure, average response size  
- Alerts: optional; start with logs + metrics only  
