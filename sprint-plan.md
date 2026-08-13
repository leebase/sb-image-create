# sb-image-create Sprint Plan

> Tactical sprint roadmap for the whole project. Keep future sprints concrete enough to guide planning, and keep the active sprint detailed enough to execute immediately.

---

## Sprint Overview

| Sprint | Focus | Status | Exit Outcome |
|--------|-------|--------|--------------|
| Sprint 1 - Foundation CLI | Contract, config, dry-run, package correctness | COMPLETE | A real paired-image CLI skeleton exists |
| Sprint 2 - Gemini Generation | Real cover + thumbnail generation | COMPLETE | One command creates both real images |
| Sprint 3 - Quality And Reproducibility | Better prompts, metadata, install confidence | ACTIVE | Output quality and reruns are more dependable |
| Sprint 4 - Expansion | Provider flexibility and workflow growth | IN PROGRESS | The tool can grow without breaking the contract |

---

## Sprint 1 - Foundation CLI

**Status:** COMPLETE  
**Goal:** Turn the documented product design into a working paired-image CLI skeleton that agents can call safely.

### Intent

By the end of Sprint 1, the project should have:
- a real `generate` command
- deterministic paired output naming
- config/default behavior
- dry-run support
- tests for the CLI contract
- a clear path to real Gemini image generation

### Scope

In scope:
- paired-output CLI contract
- Python package/bootstrap correctness
- config loading and precedence
- dry-run request resolution
- slugging and output path logic
- initial tests
- planning and architecture docs

Out of scope:
- polished prompt engineering
- production-quality image outputs
- provider abstraction beyond immediate need
- GUI or packaging work

### Tasks

| ID | Task | Status | Done When |
|----|------|--------|-----------|
| S1-T1 | Define product purpose and MVP | DONE | Product documents match the real workflow |
| S1-T2 | Create and align planning docs | DONE | `project-plan.md`, `sprint-plan.md`, `product-definition.md`, and `design.md` are coherent |
| S1-T3 | Define paired CLI contract | DONE | Inputs, outputs, naming, config, and dry-run behavior are documented |
| S1-T4 | Add image-direction skills and agent guides | DONE | Creative guidance exists as reusable project references |
| S1-T5 | Fix Python package scaffold | DONE | Package imports and console entry path are valid |
| S1-T6 | Implement dry-run paired generator | DONE | `generate` resolves a paired request without generating images |
| S1-T7 | Add CLI contract tests | DONE | Tests cover slugging, config precedence, and paired outputs |
| S1-T8 | Install-smoke the package | DONE | Editable install works; installed command verified at its install location |

### Definition Of Done

Sprint 1 is done when:
- the paired CLI contract is executable
- dry-run behavior matches the documented contract
- config defaults and CLI overrides both work
- the package can be installed and invoked as `sb-image-create`
- docs reflect actual implemented behavior

### Risks

| Risk | Response |
|------|----------|
| Dry-run and real-run behavior drift later | Share request-resolution logic between both paths |
| Config grows ad hoc | Keep the v1 schema intentionally small |
| Package setup remains fragile | Validate with an editable-install smoke test |

---

## Sprint 2 - Gemini Generation

**Status:** COMPLETE  
**Goal:** Turn the dry-run skeleton into a real paired-image generator backed by Gemini.

### Intent

By the end of Sprint 2, one command should produce:
- a real cover image
- a real related thumbnail
- machine-readable run output

### Planned Scope

- Gemini text step for story direction
- Gemini image step for cover generation
- Gemini image-edit step for thumbnail generation from the cover
- clear error handling for auth, request, and write failures
- JSON output that reflects real generation results

### Planned Tasks

| ID | Task | Status | Done When |
|----|------|--------|-----------|
| S2-T1 | Implement Gemini-backed direction generation | DONE | The app produces direction/prompt data from title and synopsis |
| S2-T2 | Implement cover image generation | DONE | The command writes a real cover image |
| S2-T3 | Implement thumbnail generation from cover | DONE | The command writes a related thumbnail derived from the cover |
| S2-T4 | Return real generation metadata in JSON | DONE | JSON reflects model usage, prompts, outputs, and metadata path |
| S2-T5 | Add integration validation for paired generation | DONE | The paired workflow is validated end to end with a real command run |

### Definition Of Done

Sprint 2 is done when:
- one command produces both real images
- the thumbnail is visibly related to the generated cover
- failures are clear and machine-readable
- the command remains callable non-interactively

### Risks

| Risk | Response |
|------|----------|
| Gemini request formats shift | Keep provider logic isolated behind internal functions |
| Thumbnail continuity is weak | Always derive the thumbnail from the generated cover |
| API failures create confusing UX | Standardize structured error output early |

---

## Sprint 3 - Quality And Reproducibility

**Status:** ACTIVE  
**Goal:** Improve output quality, debuggability, and confidence in repeated runs.

### Intent

By the end of Sprint 3, the tool should feel more dependable in real workflows, not just functional.

### Planned Scope

- richer built-in prompt logic
- metadata sidecars
- prompt/version tracking
- better validation and error handling
- install and usage confidence

### Planned Tasks

| ID | Task | Status | Done When |
|----|------|--------|-----------|
| S3-T1 | Persist paired metadata sidecars | DONE | Each run saves reproducible metadata for both outputs |
| S3-T2 | Enrich built-in prompt logic | IN PROGRESS | Direction and prompts are better than the bare skeleton baseline |
| S3-T3 | Add prompt/version metadata | DONE | Runs can be traced to the prompt logic version used |
| S3-T4 | Improve error classification | DONE | Missing auth and unsupported providers fail clearly |
| S3-T5 | Validate editable-install workflow | DONE | A clean install path is documented and tested |

### Definition Of Done

Sprint 3 is done when:
- outputs are more consistent across runs
- metadata is sufficient for debugging and reruns
- installation and execution paths are trustworthy

### Risks

| Risk | Response |
|------|----------|
| Quality improvements become endless tuning | Define “good enough” examples and stop when they are met |
| Metadata becomes noisy | Keep sidecar structure intentional and minimal |

---

## Sprint 4 - Expansion

**Status:** IN PROGRESS  
**Goal:** Extend the tool without destabilizing the core contract.

### Intent

By the end of Sprint 4, the project should be easier to evolve while keeping the CLI stable for callers.

### Planned Scope

- alternate providers such as OpenRouter
- optional style profiles or presets
- improved metadata and asset workflow support
- optional packaging/distribution improvements

### Planned Tasks

| ID | Task | Status | Done When |
|----|------|--------|-----------|
| S4-T1 | Add provider abstraction where justified | DONE | Provider dispatch exists and rejects unsupported backends clearly |
| S4-T2 | Add optional presets/style profiles | TODO | Callers can choose supported variants without ad hoc prompt changes |
| S4-T3 | Improve asset workflow support | TODO | Metadata/output handling scales to broader use |
| S4-T4 | Evaluate packaging improvements | TODO | Distribution options are documented with tradeoffs |

### Definition Of Done

Sprint 4 is done when:
- the contract remains stable while capability expands
- future enhancements no longer require redesigning the tool

---

## Current Sprint Focus

The active sprint is **Sprint 3 - Quality And Reproducibility**.

### Next Actions

1. Strengthen built-in prompt logic beyond the current baseline.
2. Improve asset workflow support and metadata depth.
3. Continue expansion without breaking the caller contract.

---

## Notes For Future Sessions

- Sprint 1 is mostly complete; avoid reopening solved contract questions unless implementation proves them wrong.
- Sprint 2 is complete; the next high-value work is quality improvement and careful expansion.
- Use this file for sprint-level sequencing and `context.md` for the immediate handoff state.
