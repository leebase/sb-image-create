# Skill: Paired Image Generation

> Use this skill when generating the actual story cover and YouTube thumbnail so they stay visually related.

---

## Purpose

This skill turns a direction artifact into two related outputs:
- `cover`
- `thumbnail`

The cover is the canonical image.
The thumbnail is derived from the cover.

---

## Required Inputs

- story title
- synopsis
- direction artifact
- output path
- requested variant

For `thumbnail`, also provide:
- cover image path or loaded cover image
- optional thumbnail title text

---

## Workflow

### Cover

1. Use the direction artifact to generate a cinematic 16:9 cover.
2. Keep the image clean enough for story/video use.
3. Save metadata so the thumbnail step can reuse the same direction.

### Thumbnail

1. Use the cover image as the source image.
2. Ask Gemini to preserve subject, palette, mood, and core scene identity.
3. Recompose for attention, contrast, and readability.
4. Add or reserve space for bold thumbnail title text.

---

## Prompt Rules

For thumbnails, include continuity instructions such as:
- preserve the same story identity
- keep the same subject and setting
- do not change the fundamental scene
- increase contrast and thumbnail readability

---

## Gemini Notes

Preferred models:
- `gemini-3-flash-preview` for direction work
- `gemini-3.1-flash-image-preview` for image generation and editing

Preferred pattern:
- generate the cover first
- generate the thumbnail from the cover image in a follow-up image edit step

---

## Quality Bar

- The cover should feel cinematic.
- The thumbnail should feel punchier, simpler, and more clickable.
- Both should obviously belong to the same story package.

---

## Avoid

- generating thumbnail and cover independently from separate prompts
- changing the main character design or scene identity
- muddy lighting or over-detailed composition

---

## Done When

The two output files look like deliberate companion assets rather than loosely related images.
