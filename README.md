# sb-image-create

`sb-image-create` is a local Python project for AI agents and automation harnesses that turns a story title and synopsis into matched image assets.

## Description

The project is aimed at a story/media pipeline where an agent needs to produce:
- a story cover image for an MP4 or story asset
- a related YouTube thumbnail

The tool should also expose the resolved visual direction so an agent or skill can understand how the story was translated into imagery and keep both outputs consistent.

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
  --variant cover \
  --name-root clockmakers-debt \
  --json
```

Output behavior:
- default output directory is the current working directory
- use `--output-dir` to write elsewhere
- filenames are derived from `--name-root`
- output files are:
  - `<name_root>_cover.jpg`
  - `<name_root>_thumb.jpg`

Example with explicit output directory:

```bash
sb-image-create generate \
  --title "The Clockmaker's Debt" \
  --synopsis "A disgraced watchmaker discovers his missing daughter is trapped in a city that trades years of life as currency." \
  --variant thumbnail \
  --name-root clockmakers-debt \
  --output-dir /abs/path/to/story-assets \
  --reference-image /abs/path/to/story-assets/clockmakers-debt_cover.jpg \
  --title-text "HE SOLD TIME TO SAVE HER" \
  --json
```

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
