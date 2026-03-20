# sb-image-create Project Plan

> **Strategic roadmap** — stable, long-term planning document
>
> For tactical execution, see `sprint-plan.md`

---

## Project Overview

**sb-image-create** is a local Python CLI for AI agents and automation harnesses to turn a story title and synopsis into reusable image direction and matched story-related image outputs.

The philosophy is **TinyClaw**:

> Build the smallest useful primitives first. Validate before scaling.

---

## Objectives

### Primary Objective
Provide a reliable local command-line tool that an agent can call to derive visual direction from a story title and synopsis, then generate a story cover image and a related YouTube thumbnail as part of a media pipeline.

### Secondary Objectives
- Keep the interface deterministic and script-friendly
- Support non-interactive authentication and execution
- Make the tool provider-agnostic enough to swap generation backends later
- Expose image-direction guidance clearly enough that an agent or skill can reuse it

---

## Non-Negotiable Constraints

- No interactive prompts during normal execution
- Caller supplies exact output path and dimensions
- Fail loudly with clear machine-readable status when requested

---

## Development Phases

### Phase 0 — Research / Bootstrap

**Status**: ACTIVE

**Goals**:
- Define the product purpose and MVP contract
- Align project memory files with the actual intended use

**Deliverables**:
- Product definition document
- Sprint plan for CLI-first implementation

---

### Phase 1 — Core Foundation

**Goal**: Ship a usable local CLI skeleton with a stable contract.

**Core components**:
1. Argument parsing and input validation
2. Story-to-direction prompt builder
3. Image generation command with dry-run and structured output

**Success Criteria**:
- An agent can call the CLI non-interactively
- The command can resolve and validate a single image generation request end to end

---

### Phase 2 — Feature Expansion

**Goal**: Improve output quality and story-asset ergonomics.

**Components**:
- Variant-aware prompting for `cover` and `thumbnail`
- Metadata sidecars and reproducibility features
- Direction output that can be reused across agent workflows

**Success Criteria**:
- Related cover and thumbnail outputs are easy to generate consistently

---

### Phase 3 — Integration & Polish

**Goal**: Make the tool production-friendly inside agent pipelines.

**Success Criteria**:
- Clear docs, stable exit behavior, and solid tests for common workflows

---

### Phase 4 — Advanced / Future (Optional)

**Potential**:
- Reference-image assisted generation
- Additional providers or model backends

*Not required for initial success.*

---

## Architecture Principles

1. **Tiny First** — smallest viable implementation
2. **Explicit State** — no hidden behavior
3. **Human Authority** — autonomy with oversight
4. **Audit Everything** — reproducible history
5. **Artifacts Over Chat** — durable outputs

---

## Core Components

### Data Stores
- `context.md` — session working memory
- `result-review.md` — running log of completed work
- `sprint-plan.md` — tactical execution plan
- `product-definition.md` — vision and constraints

---

## Risks

| Risk | Mitigation |
|------|------------|
| Scope creep | TinyClaw discipline |
| Over-complex architecture | Phase gating |
| Provider lock-in too early | Keep the CLI contract separate from backend details |
| Direction quality is inconsistent | Make resolved direction explicit and testable |

---

## Success Metrics

- A harness can derive image direction and generate both required image variants without manual steps
- The tool writes outputs exactly to requested paths
- CLI responses are parseable and dependable in automation

---

## Current Status

**Phase**: Phase 0 - Research / Bootstrap
**Mode**: Mode 2 - Collaborative
**Next Milestone**: Finalize the story-input CLI contract and begin the command skeleton

---

## Guiding Philosophy

> Build a tiny, dependable story-to-image primitive that agents can trust in production.

Keep implementations minimal. Validate before scaling.

---

*End of Project Plan*
