# sb-image-create Project Plan

> Strategic roadmap for the project. This file should stay relatively stable and explain where the project is going, why it exists, and how progress is staged.
>
> For current execution details, see `sprint-plan.md`.

---

## Project Summary

`sb-image-create` is a local Python CLI for agent harnesses and automation workflows. It takes a story title and synopsis, derives visual direction, and generates a paired set of related images:
- a `cover` image for story or MP4 usage
- a `thumbnail` image for YouTube usage

The thumbnail should feel like a stronger, more clickable version of the same visual campaign rather than a separate image.

---

## Why This Project Exists

Story pipelines need image generation that is:
- predictable
- scriptable
- reusable across sessions
- compatible with agent-driven workflows

Ad hoc prompting causes drift. Different sessions produce different visual interpretations, and the cover and thumbnail can diverge. This project creates a stable story-to-image primitive so agents can reliably generate paired assets without rebuilding the workflow every time.

---

## Primary Objective

Deliver a reliable local CLI that an agent can call from anywhere to generate a matched cover and thumbnail pair from:
- story title
- story synopsis

---

## Secondary Objectives

- Keep the interface non-interactive and automation-friendly
- Support stable defaults through `image-config.toml`
- Preserve visual continuity between cover and thumbnail
- Encode image-direction guidance into versioned application logic
- Keep backend integration swappable without redesigning the CLI contract

---

## Non-Negotiable Constraints

- Local-first CLI, no web UI dependency for MVP
- Non-interactive authentication via environment variables or config
- One invocation should generate both output images
- Output names must be predictable
- `name_root` should default to a filename-safe slug of the title
- Thumbnail text should default to the story title
- Config values should be overridable via CLI flags
- Prompt logic should live in code, not depend on runtime markdown parsing
- Fail loudly and clearly when auth, generation, or file writes fail

---

## Product Shape

### Inputs

Required:
- `title`
- `synopsis`

Common optional inputs:
- `name_root`
- `output_dir`
- cover and thumbnail dimension overrides
- config path
- JSON output flag
- dry-run flag

### Outputs

Each run should create:
- `<name_root>_cover.jpg`
- `<name_root>_thumb.jpg`

Default output location:
- the current working directory unless `output_dir` is specified

Expected supporting artifacts:
- machine-readable JSON output
- sidecar metadata for reproducibility

---

## Architecture Direction

### Prompt Logic

The project-specific creative guidance lives conceptually in:
- `skills/story-image-direction.md`
- `skills/paired-image-generation.md`
- `agents/story-art-director.md`
- `agents/thumbnail-conversion.md`

Those files are upgrade references for humans and future AI sessions.

The executable application should translate that guidance into built-in Python prompt logic. Updating the creative rules should happen through code changes, not runtime markdown loading.

### Generation Flow

1. Load built-in defaults
2. Merge config values
3. Apply CLI overrides
4. Derive story direction from title and synopsis
5. Generate the canonical cover image
6. Generate the thumbnail from the cover image
7. Save both outputs and metadata

---

## Development Phases

### Phase 0 - Bootstrap And Definition

**Goal:** Define the product clearly enough to avoid building the wrong thing.

**Success looks like:**
- project purpose documented
- design and architecture decisions recorded
- planning docs aligned with real workflow

**Status:** COMPLETE

---

### Phase 1 - Foundation CLI

**Goal:** Ship a usable paired-image CLI skeleton with stable request, naming, and config behavior.

**Core deliverables:**
- valid package layout
- `generate` command
- dry-run mode
- config loading
- slug-based output naming
- tests for CLI contract

**Success looks like:**
- a caller can resolve a paired request without image generation
- naming and output paths are predictable
- config precedence is tested

**Status:** IN PROGRESS

---

### Phase 2 - Gemini Generation

**Goal:** Turn the dry-run skeleton into a real image-producing tool.

**Core deliverables:**
- Gemini-backed direction generation
- Gemini cover generation
- Gemini thumbnail generation derived from cover
- metadata sidecars

**Success looks like:**
- one command produces both real images
- thumbnail continuity is visibly preserved
- failures are machine-readable

**Status:** PLANNED

---

### Phase 3 - Quality And Reproducibility

**Goal:** Make output quality and reruns more dependable.

**Core deliverables:**
- richer built-in prompt logic
- prompt/version metadata
- stronger error handling
- install and packaging validation

**Success looks like:**
- outputs are more consistent across runs
- generated artifacts are reproducible enough for debugging
- the tool is easy to integrate into real pipelines

**Status:** PLANNED

---

### Phase 4 - Expansion

**Goal:** Extend the tool without destabilizing the contract.

**Potential areas:**
- alternate providers such as OpenRouter
- additional presets or style profiles
- improved metadata and asset catalog support
- optional packaging/distribution improvements

**Status:** OPTIONAL

---

## Success Metrics

- A caller can generate both story images with one command
- Cover and thumbnail are recognizably related
- Output filenames are predictable without requiring explicit full paths
- JSON output is stable enough for automation
- Config defaults reduce repetitive caller boilerplate
- The CLI contract remains stable even if backends evolve

---

## Risks

| Risk | Mitigation |
|------|------------|
| Prompt quality is too weak | Encode stronger built-in prompt logic and test against realistic stories |
| Cover and thumbnail drift visually | Always derive thumbnail from the generated cover |
| Provider APIs shift | Keep provider-specific logic behind a stable internal interface |
| Config grows messy | Keep a small v1 schema and add fields deliberately |
| Project scope expands too quickly | Keep current work focused on the paired-image CLI core |

---

## Current Status

**Current Phase:** Phase 1 - Foundation CLI  
**Mode:** Collaborative  
**Next Milestone:** Gemini-backed paired generation with metadata sidecars

---

## Guiding Philosophy

> Build the smallest dependable story-to-image primitive that agents can trust in production.

Favor clarity over cleverness. Favor stable contracts over flexible ambiguity. Favor durable artifacts over chat-only knowledge.
