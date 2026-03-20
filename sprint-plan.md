# sb-image-create Sprint Plan

> Tactical plan for the current sprint. Keep this focused on concrete deliverables.

---

## Sprint 1 - Foundation CLI

**Status**: ACTIVE
**Sprint Goal**: Define and implement the first usable local CLI contract for turning story inputs into reusable image direction and generated assets.

---

## Sprint Outcomes

- Product definition written
- Project roadmap aligned to the CLI-first direction
- MVP CLI spec documented
- Story-to-image direction contract documented
- Initial implementation plan ready for coding

---

## Tasks

| ID | Task | Status | Notes |
|----|------|--------|-------|
| S1-T1 | Define product purpose and MVP | DONE | Purpose: local agent-friendly image CLI |
| S1-T2 | Create missing planning docs | DONE | `product-definition.md` and `sprint-plan.md` |
| S1-T3 | Document CLI contract and output expectations | TODO | Include title/synopsis inputs, JSON behavior, exit expectations |
| S1-T4 | Document story-to-image direction rules for agents/skills | TODO | Explain how cover and thumbnail should stay related |
| S1-T5 | Inspect package scaffold and fix bootstrap issues | TODO | Console entry point likely needs correction |
| S1-T6 | Implement initial generator command skeleton | TODO | Parse args, build direction, dry-run support |
| S1-T7 | Add tests for CLI argument behavior | TODO | Focus on contract and failure modes |

---

## Definition of Done

- Core planning docs reflect the real project purpose
- CLI contract is specific enough for Codex or another harness to call
- Direction rules are specific enough for an agent or skill to apply consistently
- First implementation task is small and unambiguous

---

## Risks

| Risk | Response |
|------|----------|
| Provider/API choice is still open | Build provider-agnostic CLI contract first |
| "Related images" is subjective | Encode shared prompt/seed/reference hooks early |
| Story interpretation may drift across runs | Make resolved direction an explicit artifact |
| Fresh scaffold may contain bootstrap mistakes | Validate package layout before implementation |

---

## Next Up

1. Document the exact CLI interface in the repo docs
2. Define the story-to-image direction artifact for agents and skills
3. Review scaffold/package structure
