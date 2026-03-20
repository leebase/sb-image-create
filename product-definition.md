# sb-image-create Product Definition

> Product-level definition for what this project is, who it serves, and what success looks like.

---

## Product Summary

`sb-image-create` is a local Python CLI for Codex and other agent harnesses. It takes a story title and synopsis, derives reusable visual direction from that story, and generates one related image asset per call.

The primary MVP workflow is two calls:
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
- a requested variant

the tool should:
1. interpret the story into visual direction
2. use the project's image-direction agents and skills to produce a variant-specific image prompt
3. generate exactly one image
4. write it to the requested path
5. expose enough structured metadata that another agent or skill can understand and reuse the same direction

---

## Required Inputs

- `--title`
- `--synopsis`
- `--variant cover|thumbnail`
- `--name-root`

---

## Optional Inputs

- `--output-dir`
- `--width`
- `--height`
- `--model`
- `--seed`
- `--reference-image`
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
- filenames should be derived from `--name-root`
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
- exactly one image written to the resolved output file path

Resolved output naming:
- `cover` writes `<output-dir>/<name_root>_cover.jpg`
- `thumbnail` writes `<output-dir>/<name_root>_thumb.jpg`
- when `--output-dir` is omitted, `<output-dir>` is the current working directory

Structured output:
- JSON on stdout when `--json` is requested

Direction artifact:
- resolved visual direction for the story
- variant-specific resolved prompt
- model and generation metadata

Likely sidecar:
- `<output>.json` containing the story inputs, resolved direction, prompt, model, seed, dimensions, and variant

---

## Direction Artifact

The tool should produce reusable direction that agents and skills can follow consistently.

That direction should be generated using the project's own reusable guidance:
- [`skills/story-image-direction.md`](/Users/lee/projects/sb-image-create/skills/story-image-direction.md)
- [`skills/paired-image-generation.md`](/Users/lee/projects/sb-image-create/skills/paired-image-generation.md)
- [`agents/story-art-director.md`](/Users/lee/projects/sb-image-create/agents/story-art-director.md)
- [`agents/thumbnail-conversion.md`](/Users/lee/projects/sb-image-create/agents/thumbnail-conversion.md)

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
2. generate a cover image at a predictable resolved output path
3. generate a related thumbnail at a predictable resolved output path
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
- predictable output naming controlled by `name_root` and optional `output_dir`
- parent directories created automatically
- story-first inputs preferred over ad hoc prompt-only input
- machine-readable behavior when requested
- loud failure on auth, generation, or file-save errors
- safe to run inside unattended agent pipelines

---

## Success Criteria

- an agent can invoke the tool without manual intervention
- title and synopsis are enough to derive usable image direction
- cover and thumbnail outputs are recognizably related
- output files are written to predictable paths without requiring the caller to pass full filenames
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
- The app should encode project-specific art direction through its skills and agent-role guidance.
- Output naming should be simple enough for unattended pipelines to predict without extra path construction.
- Predictability matters more than maximum flexibility.
- Agent ergonomics are a first-class requirement.
