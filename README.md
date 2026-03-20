# sb-image-create

`sb-image-create` is a local Python project for AI agents and automation harnesses that turns a story title and synopsis into matched image assets.

## Description

The project is aimed at a story/media pipeline where an agent needs to produce:
- a story cover image for an MP4 or story asset
- a related YouTube thumbnail

The tool should also expose the resolved visual direction so an agent or skill can understand how the story was translated into imagery and keep both outputs consistent.
The default behavior is one command that creates both images together.

## Installation

```bash
pip install -e .
```

## Usage

```bash
sb-image-create --help
```

Planned contract shape:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency." \
  --dry-run \
  --json
```

Current implementation status:
- `generate` resolves the paired request, output filenames, and dimensions
- `--dry-run` and `--json` work today
- actual Gemini image generation is the next implementation step

Output behavior:
- default output directory is the current working directory
- use `--output-dir` to write elsewhere
- `name_root` is derived automatically from the title unless overridden with `--name-root`
- output files are:
  - `<name_root>_cover.jpg`
  - `<name_root>_thumb.jpg`
- the thumbnail uses the story title as its default text
- one run creates both files

Example with explicit output directory:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency." \
  --name-root clockmakers-debt \
  --output-dir /abs/path/to/story-assets \
  --dry-run \
  --json
```

Prompt-generation behavior:
- the app uses built-in prompt logic derived from the project’s image-direction skills and agent guides
- those docs are design references for future upgrades
- the app should not need to read markdown prompt files at runtime

Config example:
- start from [`image-config.toml.example`](/Users/lee/projects/sb-image-create/image-config.toml.example)

## Development Setup

Install with development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Format code:

```bash
black src/
ruff check src/
```

## Updating Templates

To pull the latest AgentFlow templates into this project without overwriting your custom data, run:

```bash
init-agent --update
```

This will automatically detect the Python profile and refresh only the contract files: `AGENTS.md` and `skills/*`. Living project-memory files such as `context.md` and `WHERE_AM_I.md` are preserved.

---

Created on 2026-03-20 by Lee Harrington.
