# sb-image-create Session Context

> **Purpose**: Working memory for session continuity. If power drops, a new AI takes over, or we return after a break—read this first.

---

## Snapshot

| Attribute | Value |
|-----------|-------|
| **Phase** | Planning Complete / Ready for Implementation |
| **Mode** | 2 (Implementation with approval) |
| **Last Updated** | 2026-03-20 |

### Sprint Status
| Sprint | Status | Completion |
|--------|--------|------------|
| Sprint 1 — Foundation | 🟡 Active | 20% |

---

## What's Happening Now

### Current Work Stream
Defining the project purpose, MVP, and first sprint for an agent-friendly story-to-image CLI.

### Recently Completed
- ✅ Project scaffolded with init-agent
- ✅ AGENTS.md created
- ✅ Product purpose clarified
- ✅ `product-definition.md` created
- ✅ `sprint-plan.md` created
- ✅ Story title and synopsis established as primary inputs
- ✅ `design.md` created for the Gemini-first image workflow
- ✅ Initial image agent roles and project-specific skills created

### In Progress
- ⏳ Preparing the CLI contract, direction artifact, and implementation plan

---

## Decisions Locked

| Decision | Rationale | Date |
|----------|-----------|------|
| TinyClaw methodology | Build from scratch with small primitives; validate before scale | 2026-03-20 |
| Local CLI-first product shape | Enables use from Codex and other agent harnesses | 2026-03-20 |
| Story-first input contract | Title and synopsis are the right source inputs for consistent image direction | 2026-03-20 |

---

## Document Inventory

### Planning (Stable)
| File | Purpose | Status |
|------|---------|--------|
| `product-definition.md` | Product vision, constraints | ✅ Created |
| `project-plan.md` | Strategic roadmap, phases, success metrics | ✅ Updated |
| `sprint-plan.md` | Tactical execution | ✅ Created |
| `AGENTS.md` | AI agent guide, conventions, operational modes | ✅ Created |

### Session Memory (Dynamic)
| File | Purpose | Status |
|------|---------|--------|
| `context.md` | Working state, current focus, next actions | 🔄 Active |
| `result-review.md` | Running log of completed work | 🔄 Active |

### Backlog System
| File | Purpose | Status |
|------|---------|--------|
| `backlog/schema.md` | Unified backlog item schema | ⬜ To create |
| `backlog/template.md` | Copy-paste template for new backlog items | ⬜ To create |

---

## Open Questions (keep short)

1. Which image backend/provider should the first version use?
2. Should variant defaults imply standard dimensions for `cover` and `thumbnail`?
3. What exact direction artifact should the CLI expose for agents and skills?

---

## Next Actions Queue (ranked)

| Rank | Action | Owner | Done When |
|------|--------|-------|----------|
| 1 | Document exact CLI contract in repo docs | AI | Title/synopsis inputs, arguments, outputs, and behavior are explicit |
| 2 | Inspect scaffold for package/bootstrap issues | AI | Implementation can begin safely |
| 3 | Implement the first dry-run command | AI | A request can be resolved without generating an image |
| 4 | Add Gemini-backed cover generation | AI | End-to-end cover generation works |

---

## Working Conventions

### Start of session
1. Read `product-definition.md` (if exists)
2. Read this file
3. Execute the top-ranked item only
4. Update **Last Updated** if you changed any state here

### End of work unit
1. Move completed items into "Recently Completed"
2. Update "Next Actions Queue"
3. Add any new "Decisions Locked"
4. Keep "Open Questions" ≤ 5

---

## Environment Notes

- **Working Directory**: ./sb-image-create
- **Project Name**: sb-image-create
- **Profile**: Python Package
- **Author**: Lee Harrington

---

*This file is a living document—update it frequently.*
