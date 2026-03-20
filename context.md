# sb-image-create Session Context

> **Purpose**: Working memory for session continuity. If power drops, a new AI takes over, or we return after a break—read this first.

---

## Snapshot

| Attribute | Value |
|-----------|-------|
| **Phase** | Initial CLI Skeleton Implemented |
| **Mode** | 2 (Implementation with approval) |
| **Last Updated** | 2026-03-20 |

### Sprint Status
| Sprint | Status | Completion |
|--------|--------|------------|
| Sprint 1 — Foundation | 🟡 Active | 55% |

---

## What's Happening Now

### Current Work Stream
Converting the design into a working paired-image CLI skeleton with dry-run behavior and predictable output resolution.

### Recently Completed
- ✅ Project scaffolded with init-agent
- ✅ AGENTS.md created
- ✅ Product purpose clarified
- ✅ `product-definition.md` created
- ✅ `sprint-plan.md` created
- ✅ Story title and synopsis established as primary inputs
- ✅ `design.md` created for the Gemini-first image workflow
- ✅ Initial image agent roles and project-specific skills created
- ✅ Paired-output contract defined: one call creates cover + thumbnail
- ✅ `name_root` default behavior defined from title slug
- ✅ Prompt logic decision made: built into app, guided by upgradeable docs
- ✅ Valid Python package layout created (`sb_image_create`)
- ✅ `generate` dry-run command implemented
- ✅ Output path and config resolution implemented
- ✅ CLI tests added and passing with `PYTHONPATH=src pytest`
- ✅ `image-config.toml.example` created
- ✅ `architecture.md` created

### In Progress
- ⏳ Preparing the Gemini-backed generation step and richer prompt logic

---

## Decisions Locked

| Decision | Rationale | Date |
|----------|-----------|------|
| TinyClaw methodology | Build from scratch with small primitives; validate before scale | 2026-03-20 |
| Local CLI-first product shape | Enables use from Codex and other agent harnesses | 2026-03-20 |
| Story-first input contract | Title and synopsis are the right source inputs for consistent image direction | 2026-03-20 |
| One invocation creates both assets | Better fit for the real story packaging workflow | 2026-03-20 |
| Built-in prompt logic | Callable-from-anywhere behavior is more reliable than runtime markdown parsing | 2026-03-20 |
| `name_root` defaults from title slug | Reduces required arguments while keeping output filenames predictable | 2026-03-20 |
| Valid import package name `sb_image_create` | Python console entry points cannot import hyphenated module paths | 2026-03-20 |

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

1. What exact generation metadata should be persisted once Gemini image creation is live?
2. How rich should the built-in prompt templates be in v1 before adding prompt versioning?

---

## Next Actions Queue (ranked)

| Rank | Action | Owner | Done When |
|------|--------|-------|----------|
| 1 | Add Gemini-backed paired generation | AI | End-to-end cover + thumbnail generation works |
| 2 | Enrich built-in prompt logic from project guidance | AI | Direction and prompt payloads are meaningful, not placeholders |
| 3 | Persist paired metadata sidecars | AI | Runs are reproducible and debuggable |
| 4 | Package and install smoke test | AI | `sb-image-create generate` works after editable install |

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
