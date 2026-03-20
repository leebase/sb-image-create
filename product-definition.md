# sb-image-create Product Definition

> Product-level definition for what this project is, who it serves, and what success looks like.

---

## Product Summary

`sb-image-create` is a local Python CLI for Codex and other agent harnesses. It takes a story title and synopsis, derives reusable visual direction from that story, and generates a paired set of related image assets in one call.

The primary MVP workflow is one call that creates:
- one `cover` image for the story/MP4 asset
- one `thumbnail` image for YouTube

Those two outputs should feel like part of the same package.

---

## Primary User

The first user is an AI agent running inside a local content-production workflow.

Secondary users:
- Lee, running the tool directly from the terminal
- local automation scripts
- future reusable skills that need a stable story-to-image contract

---

## Problem Being Solved

Agents can generate prompts ad hoc, but that creates drift:
- different sessions may interpret the same story differently
- cover art and thumbnail art may not match
- downstream automation has no stable contract for how image direction is derived

This project solves that by making story-to-image direction explicit, reusable, and machine-friendly.

It also solves repeated invocation friction by allowing sensible defaults to live in a local image config file instead of requiring the caller to pass every option every time.

---

## Core Use Case

Given:
- a story title
- a synopsis
- an output location strategy

the tool should:
1. interpret the story into visual direction
2. use built-in project prompt logic derived from the project's image-direction agents and skills
3. generate both a cover image and a related thumbnail image
4. write them to predictable paths
5. expose enough structured metadata that another agent or skill can understand and reuse the same direction

---

## Required Inputs

- `--title`
- `--synopsis`

---

## Optional Inputs

- `--name-root`
- `--output-dir`
- `--cover-width`
- `--cover-height`
- `--thumb-width`
- `--thumb-height`
- `--model`
- `--seed`
- `--negative-prompt`
- `--json`
- `--dry-run`
- `--config`

Possible future inputs:
- `--subtitle`
- `--style-profile`
- `--metadata-output`

Raw `--prompt` input may still exist later for advanced use, but it is not the preferred MVP contract.

Default output behavior:
- if `--output-dir` is not provided, output files should be written to the current working directory
- `name_root` should default to a filename-safe slug derived from `title`
- the generated filenames should be:
  - `<name_root>_cover.jpg`
  - `<name_root>_thumb.jpg`

---

## Default Config File

The app should support a local image config file that stores default generation values so callers do not need to pass the same settings on every invocation.

That config should be able to define defaults such as:
- provider
- text model
- image model
- default width/height per variant
- default output format
- metadata behavior
- thumbnail title-text behavior
- style and prompt preferences

CLI arguments should override config values for a single run.

Priority order should be:
1. explicit CLI arguments
2. config file values
3. built-in defaults

This is part of the product contract because agent harnesses benefit from stable defaults with minimal per-call verbosity.

---

## Outputs

Primary output:
- exactly two images written to resolved output file paths

Resolved output naming:
- `cover` writes `<output-dir>/<name_root>_cover.jpg`
- `thumbnail` writes `<output-dir>/<name_root>_thumb.jpg`
- when `--output-dir` is omitted, `<output-dir>` is the current working directory

Structured output:
- JSON on stdout when `--json` is requested

Direction artifact:
- resolved visual direction for the story
- resolved prompts for both cover and thumbnail
- model and generation metadata

Likely sidecar:
- `<output>.json` containing the story inputs, resolved direction, prompt, model, seed, dimensions, and variant

---

## Direction Artifact

The tool should produce reusable direction that agents and skills can follow consistently.

That direction should be based on the project's own reusable guidance:
- [`skills/story-image-direction.md`](/Users/lee/projects/sb-image-create/skills/story-image-direction.md)
- [`skills/paired-image-generation.md`](/Users/lee/projects/sb-image-create/skills/paired-image-generation.md)
- [`agents/story-art-director.md`](/Users/lee/projects/sb-image-create/agents/story-art-director.md)
- [`agents/thumbnail-conversion.md`](/Users/lee/projects/sb-image-create/agents/thumbnail-conversion.md)

Those files are design inputs for the application and should be translated into built-in prompt logic in Python.

They should remain upgradeable over time, but the app should not depend on reading markdown files at call time.

That artifact should likely include:
- story title
- synopsis
- core subject
- setting
- mood/tone
- visual motifs
- palette guidance
- composition guidance
- forbidden or discouraged elements
- resolved prompt for `cover`
- resolved prompt for `thumbnail`

This is a product feature, not just an implementation detail.

---

## MVP Definition

The MVP is successful when an agent can:
1. pass in a title and synopsis
2. generate both a cover image and a related thumbnail in one invocation
3. write both images to predictable resolved output paths
4. receive clear success/failure behavior
5. inspect structured direction data that explains how the story became imagery
6. rely on config defaults while overriding only the values needed for the current run

The first version does not need batch workflows, a UI, or advanced editing features.

---

## Backend Strategy

Preferred initial backend:
- Gemini API

Confirmed working models during project setup:
- `gemini-3-flash-preview` for text/direction work
- `gemini-3.1-flash-image-preview` for image generation
- `gemini-2.5-flash` as a useful fallback text model

Fallback provider:
- OpenRouter

The CLI contract should stay provider-agnostic even if Gemini is the first implementation.

---

## Non-Negotiable Constraints

- local-first CLI
- non-interactive auth through environment variables or config
- support a local image config file for reusable defaults
- predictable paired-output naming controlled by derived or explicit `name_root` and optional `output_dir`
- parent directories created automatically
- story-first inputs preferred over ad hoc prompt-only input
- title should be used as the default thumbnail text input
- machine-readable behavior when requested
- loud failure on auth, generation, or file-save errors
- safe to run inside unattended agent pipelines

---

## Success Criteria

- an agent can invoke the tool without manual intervention
- title and synopsis are enough to derive usable image direction
- cover and thumbnail outputs are recognizably related
- output files are written to predictable paths without requiring the caller to pass full filenames
- `name_root` is derived automatically from the title unless explicitly overridden
- the direction artifact is inspectable and reusable
- JSON output is stable enough for automation
- backend choice does not force a CLI redesign
- common defaults can be managed centrally without breaking one-off overrides

---

## Out of Scope for MVP

- GUI or web application
- multi-image batch generation in one command
- asset catalog management
- cloud orchestration
- rich editing or inpainting workflows

---

## Product Notes

- The project is not just "an image generator."
- The story-to-direction step is part of the product.
- The app should encode project-specific art direction through built-in prompt logic derived from its skills and agent-role guidance.
- Output naming should be simple enough for unattended pipelines to predict without extra path construction.
- Predictability matters more than maximum flexibility.
- Agent ergonomics are a first-class requirement.
