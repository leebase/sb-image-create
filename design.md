# sb-image-create Design

> Technical design for the first implementation of the story-to-image CLI.

---

## Goal

Build a local Python CLI that an agent can call to turn a story title and synopsis into:
- a `cover` image suitable for use as a 16:9 MP4/story background
- a `thumbnail` image derived from that same visual concept, suitable for YouTube

The design must prioritize visual continuity between the two outputs.

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
- `--variant cover|thumbnail`
- `--name-root`

Important optional inputs:
- `--title-text`
- `--output-dir`
- `--width`
- `--height`
- `--json`
- `--dry-run`
- `--model`
- `--seed`
- `--reference-image`
- `--metadata-output`
- `--config`

Notes:
- `--title-text` is intended for thumbnail overlay text, not the story title itself
- `--reference-image` is especially important for `thumbnail`

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
- default dimensions per variant
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

Each invocation writes exactly one image to the resolved output path.

Resolved paths:
- `cover` -> `<output-dir>/<name_root>_cover.jpg`
- `thumbnail` -> `<output-dir>/<name_root>_thumb.jpg`
- if `--output-dir` is omitted, `<output-dir>` is the process current working directory

Optional machine-readable stdout:

```json
{
  "ok": true,
  "variant": "cover",
  "output": "/abs/path/to/story-001_cover.jpg",
  "model": "gemini-3.1-flash-image-preview",
  "direction": {
    "subject": "...",
    "setting": "...",
    "mood": "..."
  },
  "prompt": "...",
  "reference_image": null
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
- variant

### 2. Direction Resolution

A text model resolves the story into a reusable direction artifact.

That resolution step should be guided by the project's own image-direction resources:
- `skills/story-image-direction.md`
- `agents/story-art-director.md`

The app does not literally "execute markdown." Instead, implementation should encode the rules and output shape defined by those files so prompt-building stays aligned with project guidance.

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

The thumbnail should be created from the cover image.

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

### Cover Workflow

1. Load built-in defaults and merge with any config file values and CLI overrides
2. Use `gemini-3-flash-preview` to derive direction from title and synopsis
3. Use `gemini-3.1-flash-image-preview` to generate the cover image
4. Save the image and structured metadata

### Thumbnail Workflow

1. Load built-in defaults and merge with any config file values and CLI overrides
2. Resolve the same direction artifact
3. Load the cover image from `--reference-image` or a known paired asset path
4. Send the cover image plus thumbnail instructions to `gemini-3.1-flash-image-preview`
5. Ask Gemini to preserve scene identity while optimizing for thumbnail use
6. Save the thumbnail and structured metadata

Important prompt rule:
- explicitly instruct Gemini not to change the core scene identity when generating the thumbnail

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
- reserve or include space for bold viral title text
- do not change the fundamental scene

---

## CLI Shape

Planned command shape:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency." \
  --variant cover \
  --config /abs/path/to/image-config.toml \
  --name-root clockmakers-debt \
  --output-dir /abs/path/to/story-assets \
  --json
```

Thumbnail example:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency." \
  --variant thumbnail \
  --config /abs/path/to/image-config.toml \
  --reference-image /abs/path/to/cover.png \
  --title-text "HE SOLD TIME TO SAVE HER" \
  --name-root clockmakers-debt \
  --output-dir /abs/path/to/story-assets \
  --json
```

Minimal call shape when config defaults are present:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency." \
  --variant cover \
  --name-root clockmakers-debt
```

---

## Error Handling

The command should fail clearly when:
- auth is missing
- the Gemini request fails
- the model name is invalid
- the config file is unreadable or invalid
- the resolved output directory cannot be created
- thumbnail generation is requested without a usable source image

When `--json` is enabled, failures should still be machine-readable.

---

## Implementation Plan

### Phase 1

Build a dry-run capable CLI that:
- parses inputs
- validates required fields
- loads config defaults
- applies CLI overrides
- resolves output directory and output filename
- resolves direction from story inputs
- prints the resolved request as JSON

### Phase 2

Add Gemini text-model integration for direction generation.

### Phase 3

Add Gemini image generation for `cover`.

### Phase 4

Add Gemini image editing flow for `thumbnail` using `--reference-image`.

### Phase 5

Add tests for:
- CLI argument validation
- config loading and override precedence
- output path resolution from `name_root` and `output_dir`
- dry-run behavior
- metadata shape
- thumbnail requiring source continuity inputs

---

## Open Design Questions

- Should the CLI auto-discover the paired cover image when generating a thumbnail?
- Should title text be rendered by Gemini directly, or should the first version only reserve space for text?
- Should the direction artifact be persisted separately from per-image metadata?
- Should default dimensions be strict per variant or overridable with warnings?
- Should config values support named presets in addition to plain defaults?

---

## Recommendation

Start with the simplest dependable path:
- generate a clean 16:9 cover first
- require `--reference-image` for thumbnail generation
- ask Gemini to transform the cover into a thumbnail variant
- keep title text support simple in the first pass

This minimizes drift and gives the project the strongest chance of producing genuinely related outputs from day one.
