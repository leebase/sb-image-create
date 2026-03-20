"""CLI entry point for sb-image-create."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

from sb_image_create import __version__

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback behavior
    import tomli as tomllib


DEFAULT_CONFIG_PATH = "image-config.toml"


@dataclass
class AssetSpec:
    path: str
    width: int
    height: int


@dataclass
class DryRunResult:
    ok: bool
    title: str
    synopsis: str
    name_root: str
    output_dir: str
    thumbnail_text: str
    config_path: str | None
    outputs: dict[str, AssetSpec]


def slugify_title(value: str) -> str:
    """Create a filesystem-safe slug from a title."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise ValueError("Unable to derive a safe name_root from title")
    return slug


def load_config(path: Optional[Path]) -> dict[str, Any]:
    """Load TOML config if present."""
    if path is None:
        return {}
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def resolve_output_dir(output_dir: Optional[str]) -> Path:
    """Resolve output directory, defaulting to the current working directory."""
    if output_dir:
        return Path(output_dir).expanduser().resolve()
    return Path.cwd().resolve()


def resolve_dimensions(
    config: dict[str, Any],
    cover_width: int | None,
    cover_height: int | None,
    thumb_width: int | None,
    thumb_height: int | None,
) -> dict[str, tuple[int, int]]:
    """Resolve dimensions from CLI overrides, config, then built-in defaults."""
    defaults = {
        "cover": {"width": 1920, "height": 1080},
        "thumbnail": {"width": 1280, "height": 720},
    }
    config_images = config.get("images", {})
    cover_config = config_images.get("cover", {})
    thumb_config = config_images.get("thumbnail", {})

    return {
        "cover": (
            cover_width or cover_config.get("width") or defaults["cover"]["width"],
            cover_height or cover_config.get("height") or defaults["cover"]["height"],
        ),
        "thumbnail": (
            thumb_width
            or thumb_config.get("width")
            or defaults["thumbnail"]["width"],
            thumb_height
            or thumb_config.get("height")
            or defaults["thumbnail"]["height"],
        ),
    }


def build_dry_run_result(args: argparse.Namespace) -> DryRunResult:
    """Build the resolved request shape for the paired image generation command."""
    config_path = Path(args.config).expanduser().resolve() if args.config else None
    config = load_config(config_path)

    output_dir = resolve_output_dir(
        args.output_dir or config.get("output", {}).get("directory")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    name_root = args.name_root or slugify_title(args.title)
    thumbnail_text = args.title_text or args.title
    dimensions = resolve_dimensions(
        config,
        args.cover_width,
        args.cover_height,
        args.thumb_width,
        args.thumb_height,
    )

    cover_path = output_dir / f"{name_root}_cover.jpg"
    thumb_path = output_dir / f"{name_root}_thumb.jpg"

    return DryRunResult(
        ok=True,
        title=args.title,
        synopsis=args.synopsis,
        name_root=name_root,
        output_dir=str(output_dir),
        thumbnail_text=thumbnail_text,
        config_path=str(config_path) if config_path else None,
        outputs={
            "cover": AssetSpec(
                path=str(cover_path),
                width=dimensions["cover"][0],
                height=dimensions["cover"][1],
            ),
            "thumbnail": AssetSpec(
                path=str(thumb_path),
                width=dimensions["thumbnail"][0],
                height=dimensions["thumbnail"][1],
            ),
        },
    )


def cmd_generate(args: argparse.Namespace) -> int:
    """Handle the generate command."""
    result = build_dry_run_result(args)
    payload = asdict(result)

    if args.dry_run or args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print("Generation is not implemented yet. Re-run with --dry-run or --json.")
    return 2


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        prog="sb-image-create",
        description="Generate related story cover and thumbnail assets.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser(
        "generate",
        help="Resolve a paired generation request from title and synopsis.",
    )
    generate.add_argument("--title", required=True, help="Story title.")
    generate.add_argument("--synopsis", required=True, help="Story synopsis.")
    generate.add_argument(
        "--title-text",
        help="Optional thumbnail text override. Defaults to the story title.",
    )
    generate.add_argument(
        "--name-root",
        help="Optional filename root. Defaults to a slug derived from --title.",
    )
    generate.add_argument(
        "--output-dir",
        help="Optional output directory. Defaults to the current working directory.",
    )
    generate.add_argument(
        "--cover-width",
        type=int,
        help="Optional cover width override.",
    )
    generate.add_argument(
        "--cover-height",
        type=int,
        help="Optional cover height override.",
    )
    generate.add_argument(
        "--thumb-width",
        type=int,
        help="Optional thumbnail width override.",
    )
    generate.add_argument(
        "--thumb-height",
        type=int,
        help="Optional thumbnail height override.",
    )
    generate.add_argument(
        "--config",
        default=DEFAULT_CONFIG_PATH,
        help=(
            "Path to image config TOML. Defaults to image-config.toml in the current "
            "working directory."
        ),
    )
    generate.add_argument(
        "--json",
        action="store_true",
        help="Print the resolved request as JSON.",
    )
    generate.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve inputs and output paths without generating images.",
    )
    generate.set_defaults(func=cmd_generate)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
