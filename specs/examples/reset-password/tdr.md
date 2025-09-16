# Technical Design Review (TDR) — Reset Password Flow

**Author**: Example  
**Date**: 2025-09-15  
**Links**: Spec (`spec.md`)

---

## 1. Summary
Implement a secure password reset flow using time-limited tokens and email delivery, ensuring no user enumeration and a simple UX.

## 2. Decision Drivers & Non‑Goals
- Drivers: security, simplicity, low support overhead
- Non‑Goals: social login reset, MFA reset

## 3. Current State — Codebase Map (concise)
- Auth service handles login/register; no reset flow exists
- Email provider integration in place for notifications

## 4. Proposed Design (high level, implementation‑agnostic)
- Endpoint to request reset: always return generic success
- Generate signed, time-limited token; store one active token per user
- Email link with token; confirmation endpoint validates token and updates password
- Rate limit reset requests

## 5. Alternatives Considered
- Magic-link login instead of reset — not chosen (different UX)
- Short-lived OTP via SMS — adds cost and complexity

## 6. Data Model & Contract Changes
- Token store (table or cache) with user_id, token_hash, expires_at, used_at
- New endpoints as defined in Impact Analysis
- Backward compatible (additive)

## 7. Security, Privacy, Compliance
- No email enumeration; generic responses
- Token signed and hashed at rest; single-use; short TTL (e.g., 30m)
- Brute-force protection via rate limiting

## 8. Observability & Operations
- Logs/metrics as in Impact Analysis
- Dashboard for success rate and failures
- Alerts on unusual volume or failure spikes

## 9. Rollout & Migration
- Feature flag `auth.reset_password.enabled`
- No data backfill required
- Revert: disable flag, clear active tokens

## 10. Test Strategy & Spec Coverage (TDD)
- TDD: failing tests → implement → refactor
- Spec→Test mapping:
  - AC-1: email delivered for valid user → integration test
  - AC-2: expired token shows error → unit + integration
  - AC-3: unknown email yields generic success → unit test
- Negative & edge cases: reused token, tampered token
- CI: tests must run and block merge

## 11. Risks & Open Questions
- Email deliverability variance
- Token TTL tuning

## 12. Milestones / Plan (post‑approval)
- M1: Request endpoint + email send (tests green)
- M2: Confirm endpoint + password update (tests green)
- M3: Rate limiting, observability, docs (tests green)

---

**Approval Gate**: Do not start coding until this TDR is reviewed and approved in the PR.
