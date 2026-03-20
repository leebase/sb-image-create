# WHERE_AM_I — sb-image-create

> **Product-level orientation.** Where does this project stand against its goals?
>
> This file tracks progress toward the product vision. For session-level context (what was I working on?), see `context.md`.

---

## Project Health

| Attribute | Value |
|-----------|-------|
| **Project** | sb-image-create |
| **Profile** | Python Package |
| **Current Phase** | Phase 0 — Bootstrap |
| **Overall Status** | 🟡 Purpose defined, implementation not started |
| **Last Updated** | 2026-03-20 |

---

## Progress Against Product Goals

> Reference: `product-definition.md` for full success criteria.

### MVP Criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Agent-callable image CLI | 🟡 Defined | Product and sprint docs now aligned |
| Related cover + thumbnail workflow | ⬜ Not started | CLI implementation still pending |
| Basic documentation | ✅ Done | Scaffolded by init-agent |

### Current Phase Goals

| Goal | Status | Notes |
|------|--------|-------|
| Establish project structure | ✅ Done | |
| Define product vision | ✅ Done | `product-definition.md` created |
| First working feature | ⬜ Not started | |

---

## Sprint Position

| Sprint | Focus | Status |
|--------|-------|--------|
| Sprint 1 — Foundation | CLI contract and first implementation slice | 🟡 Active |

---

## Product Risks & Blockers

| Risk/Blocker | Impact | Status |
|-------------|--------|--------|
| Provider/backend choice not yet locked | Implementation details may shift | 🟡 Manageable |
| Missing CLI implementation | No usable output yet | 🟡 Action needed |

---

## Key Decisions Made

Decisions that affect product direction (for technical decisions, see `architecture.md`):

| Decision | Rationale | Date |
|----------|-----------|------|
| Python Package profile selected | Best fit for project goals | 2026-03-20 |
| Local CLI-first approach | Best fit for Codex and other agent harnesses | 2026-03-20 |

---

## What "Done" Looks Like

> Pull from `product-definition.md` once written. This section answers: "How do we know we've succeeded?"

- [ ] MVP criteria met
- [ ] Agents can generate a cover image to an exact output path
- [ ] Agents can generate a related YouTube thumbnail to an exact output path
- [ ] Documentation complete

---

*Update this file when project milestones are reached or product direction changes. This is your compass — `context.md` is your GPS.*
