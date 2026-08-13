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
| **Current Phase** | Phase 3 — Quality And Reproducibility |
| **Overall Status** | 🟡 Live Gemini flow validated; quality and expansion work active |
| **Last Updated** | 2026-03-20 |

---

## Progress Against Product Goals

> Reference: `product-definition.md` for full success criteria.

### MVP Criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Agent-callable image CLI | ✅ Done | Dry-run, install smoke, and global command verification exist |
| Related cover + thumbnail workflow | ✅ Done | Live Gemini flow generated both assets and metadata |
| Basic documentation | ✅ Done | Scaffolded by init-agent |

### Current Phase Goals

| Goal | Status | Notes |
|------|--------|-------|
| Establish project structure | ✅ Done | |
| Define product vision | ✅ Done | `product-definition.md` created |
| First working feature | ✅ Done | Dry-run paired generator and install smoke exist |

---

## Sprint Position

| Sprint | Focus | Status |
|--------|-------|--------|
| Sprint 1 — Foundation | Paired CLI contract and first implementation slice | ✅ Complete |
| Sprint 2 — Gemini Generation | Real paired-image production | ✅ Complete |
| Sprint 3 — Quality And Reproducibility | Better metadata and prompt traceability | 🟡 Active |
| Sprint 4 — Expansion | Provider flexibility groundwork | 🟡 In Progress |

---

## Product Risks & Blockers

| Risk/Blocker | Impact | Status |
|-------------|--------|--------|
| Prompt logic still needs code-level enrichment | Image quality work remains | 🟡 Manageable |
| Alternate provider support not yet implemented | Expansion remains partial | 🟡 Manageable |

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
