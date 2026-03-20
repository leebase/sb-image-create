# Skill: Story Image Direction

> Use this skill when you need to turn a story title and synopsis into compelling visual direction for image generation.

---

## What This Skill Does

This skill helps derive a reusable direction artifact that can guide both:
- a cinematic story cover
- a related YouTube thumbnail

Use it before image generation, not after.

---

## Inputs

- story title
- synopsis
- target variant if only one image is being prepared

---

## Output Shape

Produce a direction artifact with:
- `subject`
- `setting`
- `mood`
- `motifs`
- `palette`
- `composition`
- `continuity_rules`
- `cover_prompt`
- `thumbnail_prompt`

Keep it compact and concrete.

---

## Workflow

1. Read the title and synopsis closely.
2. Identify the single strongest visual hook.
3. Choose one dominant emotional tone.
4. Pick 2-4 motifs that support the story without overcrowding the frame.
5. Describe the cover as a cinematic widescreen composition.
6. Describe the thumbnail as the same story package with stronger readability and title-safe space.

---

## Heuristics

- Prefer one memorable focal subject over many details.
- Use the synopsis to infer stakes, not to illustrate every event.
- Choose images that communicate genre and tension instantly.
- Make the direction easy for another agent to reuse later.
- If the story has a human protagonist, keep the character depiction consistent across variants.

---

## Cover Guidance

The `cover_prompt` should aim for:
- cinematic 16:9 framing
- strong atmosphere
- clean composition
- no text embedded in the image by default
- suitability as an MP4/story background

---

## Thumbnail Guidance

The `thumbnail_prompt` should aim for:
- same subject and scene identity as the cover
- higher contrast and stronger focal emphasis
- room for bold title text
- emotional immediacy
- better legibility at small sizes

Use language that preserves continuity, such as:
- keep the same subject, setting, palette, and mood
- do not change the core scene identity

---

## Avoid

- generic prompt filler
- contradictory style terms
- overcrowded symbolism
- changing the scene between cover and thumbnail

---

## Done When

Another agent can read the direction artifact and generate both image variants without guessing what should stay constant.
