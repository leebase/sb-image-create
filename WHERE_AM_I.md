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
| **Current Phase** | Phase 1 — Core Foundation |
| **Overall Status** | 🟡 Dry-run CLI implemented, Gemini generation pending |
| **Last Updated** | 2026-03-20 |

---

## Progress Against Product Goals

> Reference: `product-definition.md` for full success criteria.

### MVP Criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Agent-callable image CLI | 🟡 In progress | Dry-run command and output resolution implemented |
| Related cover + thumbnail workflow | 🟡 Designed | Generation flow documented, implementation pending |
| Basic documentation | ✅ Done | Scaffolded by init-agent |

### Current Phase Goals

| Goal | Status | Notes |
|------|--------|-------|
| Establish project structure | ✅ Done | |
| Define product vision | ✅ Done | `product-definition.md` created |
| First working feature | 🟡 In progress | Dry-run paired generator skeleton exists |

---

## Sprint Position

| Sprint | Focus | Status |
|--------|-------|--------|
| Sprint 1 — Foundation | Paired CLI contract and first implementation slice | 🟡 Active |

---

## Product Risks & Blockers

| Risk/Blocker | Impact | Status |
|-------------|--------|--------|
| Full Gemini generation not yet implemented | No final images yet | 🟡 Action needed |
| Prompt logic still needs code-level enrichment | Image quality work remains | 🟡 Manageable |

---

## Key Decisions Made

Decisions that affect product direction (for technical decisions, see `architecture.md`):

| Decision | Rationale | Date |
|----------|-----------|------|
| Python Package profile selected | Best fit for project goals | 2026-03-20 |
| Local CLI-first approach | Best fit for Codex and other agent harnesses | 2026-03-20 |
| One invocation creates both assets | Best fit for story packaging workflow | 2026-03-20 |

---

## What "Done" Looks Like

> Pull from `product-definition.md` once written. This section answers: "How do we know we've succeeded?"

- [ ] MVP criteria met
- [ ] Agents can generate a cover image to a predictable output path
- [ ] Agents can generate a related YouTube thumbnail to a predictable output path
- [ ] Documentation complete

---

*Update this file when project milestones are reached or product direction changes. This is your compass — `context.md` is your GPS.*
