# PR Checklist

- [ ] Attached **Spec** folder under `/specs/<feature>/` (must include `spec.md`)
- [ ] Referenced **Agent Technical Context** (`/docs/agent_context.md`)
- [ ] Followed **Agent Operating Procedure** (`/docs/agent_operating_procedure.md`)
- [ ] **Impact Analysis** saved at `/specs/<feature>/impact.md`
- [ ] **TDR** created at `/specs/<feature>/tdr.md` and approved
- [ ] **TDD**: added failing tests first, then implementation
- [ ] Mapped Spec acceptance criteria → Test IDs in the TDR
- [ ] Added/updated observability (logs/metrics/dashboards) if needed
- [ ] Security & privacy reviewed (secrets, PII, authZ/authN)
- [ ] Rollback plan documented
