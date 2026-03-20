# sb-image-create Sprint Plan

> Tactical execution plan for the current sprint. This file should make the next unit of work obvious.

---

## Sprint 1 - Foundation CLI

**Status:** ACTIVE  
**Sprint Goal:** Turn the documented product design into a working paired-image CLI skeleton that agents can call safely.

---

## Sprint Intent

By the end of this sprint, the project should have:
- a real `generate` command
- deterministic output naming
- config/default behavior
- dry-run support
- a clear path to real Gemini image generation

This sprint is about making the contract executable, not about perfect image quality yet.

---

## Scope

### In Scope

- paired-output CLI contract
- Python package/bootstrap correctness
- config loading and precedence
- dry-run request resolution
- slugging and output path logic
- initial tests
- planning and architecture docs

### Out Of Scope

- polished prompt engineering
- production-quality image outputs
- provider abstraction layers beyond what is needed now
- GUI or packaging work

---

## Tasks

| ID | Task | Status | Done When |
|----|------|--------|-----------|
| S1-T1 | Define product purpose and MVP | DONE | Product documents match the real workflow |
| S1-T2 | Create and align planning docs | DONE | `project-plan.md`, `sprint-plan.md`, `product-definition.md`, and `design.md` are coherent |
| S1-T3 | Define paired CLI contract | DONE | Inputs, outputs, naming, config, and dry-run behavior are documented |
| S1-T4 | Add image-direction skills and agent guides | DONE | Creative guidance exists as reusable project references |
| S1-T5 | Fix Python package scaffold | DONE | Package imports and console entry path are valid |
| S1-T6 | Implement dry-run paired generator | DONE | `generate` resolves a paired request without generating images |
| S1-T7 | Add CLI contract tests | DONE | Tests cover slugging, config precedence, and paired outputs |
| S1-T8 | Implement Gemini-backed paired generation | TODO | One command produces both real images |
| S1-T9 | Persist metadata sidecars | TODO | Run data is saved for reproducibility and debugging |
| S1-T10 | Install-smoke the package | TODO | `sb-image-create generate` works after editable install |

---

## Current Deliverables

### Already Delivered

- planning docs
- product definition
- design doc
- architecture doc
- valid `sb_image_create` package
- `generate` dry-run command
- config example
- initial tests

### Still Needed To Close The Sprint

- real Gemini generation
- metadata sidecars
- editable-install smoke test

---

## Definition Of Done

Sprint 1 is done when:
- one `generate` command creates both real images
- output naming matches the documented contract
- config defaults and CLI overrides both work
- metadata is written for the run
- the package can be installed and invoked as `sb-image-create`
- docs reflect the actual implemented behavior

---

## Risks And Watchouts

| Risk | Response |
|------|----------|
| Gemini integration changes request shape | Keep the CLI stable and adapt internal implementation only |
| Prompt quality is still shallow | Improve built-in prompt logic after the real generation loop works |
| Metadata shape grows ad hoc | Define the sidecar structure before implementation |
| Dry-run and real-run behavior diverge | Keep both paths sharing the same resolution logic |

---

## Next Actions

1. Implement Gemini-backed paired generation.
2. Define and persist the metadata sidecar format.
3. Install the package in editable mode and smoke test the real CLI command.

---

## Notes For The Next Session

- The foundation work is no longer speculative; there is a working dry-run CLI.
- The next meaningful milestone is real image generation, not more planning.
- Preserve the current contract unless there is a strong reason to change it.
