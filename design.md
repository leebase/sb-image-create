# sb-image-create Design

> Technical design for the first implementation of the story-to-image CLI.

---

## Goal

Build a local Python CLI that an agent can call to turn a story title and synopsis into:
- a `cover` image suitable for use as a 16:9 MP4/story background
- a `thumbnail` image derived from that same visual concept, suitable for YouTube

The design must prioritize visual continuity between the two outputs.
The default user experience should be one invocation that creates both outputs.

---

## Core Product Rule

The two images must be related.

For the first implementation, "related" does not mean "prompted similarly." It means:
- the `cover` is generated first as the canonical story image
- the `thumbnail` is generated from that cover image as an edit/transform
- the thumbnail preserves the same scene identity, subject, palette, and mood
- the thumbnail is recomposed for clickability and can include title text

This mirrors the strongest Gemini-native workflow we identified: generate a base image, then iterate from it in the same conversation or with the first image supplied back as reference.

---

## Backend Choice

Primary provider:
- Gemini API

Confirmed working models:
- `gemini-3-flash-preview` for story interpretation and prompt/direction work
- `gemini-3.1-flash-image-preview` for image generation and image editing
- `gemini-2.5-flash` as a fallback text model

Fallback provider:
- OpenRouter

The CLI surface should remain provider-agnostic even though Gemini is the first target.

---

## User Inputs

Required:
- `--title`
- `--synopsis`

Important optional inputs:
- `--title-text`
- `--name-root`
- `--output-dir`
- `--cover-width`
- `--cover-height`
- `--thumb-width`
- `--thumb-height`
- `--json`
- `--dry-run`
- `--model`
- `--seed`
- `--metadata-output`
- `--config`

Notes:
- `--title-text` defaults to the story title
- `--name-root` defaults to a filename-safe slug derived from the story title

Default output behavior:
- if `--output-dir` is omitted, use the current working directory
- derive filenames from `--name-root`
- resolved filenames:
  - `<name_root>_cover.jpg`
  - `<name_root>_thumb.jpg`

---

## Config File Design

The CLI should support a local image config file so repeated calls do not need to pass the same operational settings every time.

Suggested default path:
- `image-config.toml`

Possible future supported locations:
- explicit `--config /abs/path/to/image-config.toml`
- project-root default config

The config file should define reusable defaults such as:
- provider
- text model
- image model
- default dimensions for cover and thumbnail
- output format
- metadata sidecar behavior
- style defaults
- prompt preferences
- default thumbnail title handling

Suggested precedence:
1. explicit CLI flags
2. config file values
3. hard-coded application defaults

This keeps the CLI terse for automation while preserving override flexibility.

---

## Output Contract

Each invocation writes exactly two images to resolved output paths.

Resolved paths:
- `cover` -> `<output-dir>/<name_root>_cover.jpg`
- `thumbnail` -> `<output-dir>/<name_root>_thumb.jpg`
- if `--output-dir` is omitted, `<output-dir>` is the process current working directory

Optional machine-readable stdout:

```json
{
  "ok": true,
  "outputs": {
    "cover": "/abs/path/to/story-001_cover.jpg",
    "thumbnail": "/abs/path/to/story-001_thumb.jpg"
  },
  "model": "gemini-3.1-flash-image-preview",
  "direction": {
    "subject": "...",
    "setting": "...",
    "mood": "..."
  },
  "prompts": {
    "cover": "...",
    "thumbnail": "..."
  }
}
```

Likely sidecar metadata:
- `<output>.json`

That metadata should be sufficient for:
- debugging
- re-running the generation
- generating the paired image later

---

## Artifact Flow

### 1. Story Inputs

Input:
- story title
- synopsis
- derived title text
- derived or explicit name root

### 2. Direction Resolution

A text model resolves the story into a reusable direction artifact.

That resolution step should be based on the project's own image-direction resources:
- `skills/story-image-direction.md`
- `agents/story-art-director.md`

The app should not read these markdown files at runtime.
Instead, implementation should encode the rules and output shape defined by those files into built-in Python prompt logic so the application is portable and callable from anywhere.

When the skills or agent guidance change, the app should be updated to match and redeployed.

Suggested fields:
- story title
- synopsis
- subject
- setting
- mood
- motifs
- palette
- composition guidance
- do-not-include guidance
- cover prompt
- thumbnail prompt template

### 3. Cover Generation

The cover is the canonical image.

Requirements:
- cinematic 16:9 composition
- strong focal subject
- suitable as a background image for HD video
- no overlaid text in the base cover image unless explicitly requested later

### 4. Thumbnail Generation

The thumbnail should be created from the generated cover image in the same command flow.

That step should be guided by:
- `skills/paired-image-generation.md`
- `agents/thumbnail-conversion.md`

Requirements:
- preserve the visual identity of the cover
- increase readability and contrast at small size
- allow bold title text or a title-safe region
- remain recognizably the same story package

---

## Variant Strategy

### Cover

Intended use:
- MP4/story background

Preferred characteristics:
- widescreen composition
- enough negative space for video overlays if needed
- strong atmosphere
- readable subject at a glance

Default target:
- 16:9
- implementation default may be `1920x1080`
- Gemini-native generation may use a larger 16:9 size and then downscale

### Thumbnail

Intended use:
- YouTube thumbnail

Preferred characteristics:
- same scene identity as cover
- stronger focal emphasis
- higher contrast
- room for large attention-grabbing title text
- optimized for small preview size

Default target:
- 16:9
- implementation default may be `1280x720`

---

## Gemini Workflow

### Paired Workflow

1. Load built-in defaults and merge with any config file values and CLI overrides
2. Derive `name_root` from the title unless explicitly provided
3. Derive thumbnail title text from the story title unless explicitly provided
4. Use `gemini-3-flash-preview` to derive direction from title and synopsis
5. Use `gemini-3.1-flash-image-preview` to generate the cover image
6. Use the generated cover image as the source for thumbnail generation
7. Ask Gemini to preserve scene identity while optimizing for thumbnail use and incorporating title text
8. Save both images and structured metadata

Important prompt rule:
- explicitly instruct Gemini not to change the core scene identity when generating the thumbnail
- explicitly tell Gemini to include the title text in the thumbnail output

---

## Prompting Rules

The system should produce prompts that are explicit about:
- who or what the main subject is
- what emotional tone the image should carry
- what visual motifs matter
- what should stay constant between cover and thumbnail
- what should change for thumbnail readability

Thumbnail prompts should include language like:
- keep the same subject, palette, mood, and setting
- preserve the same story identity
- increase clarity and contrast for thumbnail readability
- include the story title as bold thumbnail text
- do not change the fundamental scene

---

## CLI Shape

Planned command shape:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency." \
  --config /abs/path/to/image-config.toml \
  --output-dir /abs/path/to/story-assets \
  --json
```

Minimal call shape when config defaults are present:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency."
```

---

## Error Handling

The command should fail clearly when:
- auth is missing
- the Gemini request fails
- the model name is invalid
- the config file is unreadable or invalid
- the resolved output directory cannot be created
- `name_root` cannot be derived safely from the title

When `--json` is enabled, failures should still be machine-readable.

---

## Implementation Plan

### Phase 1

Build a dry-run capable CLI that:
- parses inputs
- validates required fields
- loads config defaults
- applies CLI overrides
- derives `name_root` and title text defaults
- resolves paired output paths
- resolves direction from story inputs
- prints the resolved request as JSON

### Phase 2

Add Gemini text-model integration for direction generation.

### Phase 3

Add Gemini image generation for `cover`.

### Phase 4

Add Gemini image editing flow for `thumbnail` using the generated cover as input.

### Phase 5

Add tests for:
- CLI argument validation
- config loading and override precedence
- output path resolution from derived `name_root` and `output_dir`
- title slugging behavior
- dry-run behavior
- metadata shape
- paired generation flow

---

## Open Design Questions

- Should the direction artifact be persisted separately from per-image metadata?
- Should default dimensions be strict per variant or overridable with warnings?
- Should config values support named presets in addition to plain defaults?

---

## Recommendation

Start with the simplest dependable path:
- generate a clean 16:9 cover first
- derive the thumbnail from that cover in the same command
- default the thumbnail text to the story title
- keep prompt logic built into the app and versioned in code

This minimizes drift and gives the project the strongest chance of producing genuinely related outputs from day one.
