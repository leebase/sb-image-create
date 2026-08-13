"""CLI entry point for sb-image-create."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional

from sb_image_create import __version__

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback behavior
    import tomli as tomllib


DEFAULT_CONFIG_PATH = "image-config.toml"
DEFAULT_PROVIDER = "gemini"
DEFAULT_TEXT_MODEL = "gemini-3-flash-preview"
DEFAULT_IMAGE_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_COVER_WIDTH = 1920
DEFAULT_COVER_HEIGHT = 1080
DEFAULT_THUMB_WIDTH = 1280
DEFAULT_THUMB_HEIGHT = 720
PROMPT_LOGIC_VERSION = "v2"


class CliError(RuntimeError):
    """Raised for predictable CLI failures."""


@dataclass
class AssetSpec:
    path: str
    width: int
    height: int


@dataclass
class ResolvedRequest:
    ok: bool
    title: str
    synopsis: str
    name_root: str
    output_dir: str
    cover_title_text: str
    thumbnail_text: str
    subtitle: Optional[str]
    config_path: str | None
    provider: str
    text_model: str
    image_model: str
    outputs: dict[str, AssetSpec]


@dataclass
class GenerationResult:
    ok: bool
    title: str
    synopsis: str
    name_root: str
    output_dir: str
    cover_title_text: str
    thumbnail_text: str
    subtitle: Optional[str]
    models: dict[str, str]
    outputs: dict[str, AssetSpec]
    direction: dict[str, Any]
    prompts: dict[str, str]
    metadata_path: str


@dataclass
class RunMetadata:
    ok: bool
    provider: str
    prompt_logic_version: str
    title: str
    synopsis: str
    name_root: str
    output_dir: str
    cover_title_text: str
    thumbnail_text: str
    subtitle: Optional[str]
    config_path: Optional[str]
    models: dict[str, str]
    requested_outputs: dict[str, AssetSpec]
    direction: dict[str, Any]
    prompts: dict[str, str]
    metadata_path: str


def slugify_title(value: str) -> str:
    """Create a filesystem-safe slug from a title."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise CliError("Unable to derive a safe name_root from title")
    return slug


def load_config(path: Optional[Path]) -> dict[str, Any]:
    """Load TOML config if present."""
    if path is None or not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_dotenv(path: Path) -> None:
    """Load simple KEY=VALUE pairs from a local .env file into the environment."""
    if not path.exists():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def resolve_output_dir(output_dir: Optional[str]) -> Path:
    """Resolve output directory, defaulting to the current working directory."""
    if output_dir:
        return Path(output_dir).expanduser().resolve()
    return Path.cwd().resolve()


def resolve_dimensions(
    config: dict[str, Any],
    cover_width: Optional[int],
    cover_height: Optional[int],
    thumb_width: Optional[int],
    thumb_height: Optional[int],
) -> dict[str, tuple[int, int]]:
    """Resolve dimensions from CLI overrides, config, then built-in defaults."""
    defaults = {
        "cover": {"width": DEFAULT_COVER_WIDTH, "height": DEFAULT_COVER_HEIGHT},
        "thumbnail": {
            "width": DEFAULT_THUMB_WIDTH,
            "height": DEFAULT_THUMB_HEIGHT,
        },
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


def resolve_models(
    config: dict[str, Any],
    text_model_override: Optional[str],
    image_model_override: Optional[str],
) -> dict[str, str]:
    """Resolve model names from config and CLI overrides."""
    config_models = config.get("models", {})
    return {
        "text": text_model_override or config_models.get("text") or DEFAULT_TEXT_MODEL,
        "image": image_model_override
        or config_models.get("image")
        or DEFAULT_IMAGE_MODEL,
    }


def resolve_provider(config: dict[str, Any], provider_override: Optional[str]) -> str:
    """Resolve provider from config and CLI overrides."""
    return provider_override or config.get("provider") or DEFAULT_PROVIDER


def build_resolved_request(args: argparse.Namespace) -> ResolvedRequest:
    """Build the resolved request shape for the paired image generation command."""
    config_path = Path(args.config).expanduser().resolve() if args.config else None
    config = load_config(config_path)

    output_dir = resolve_output_dir(
        args.output_dir or config.get("output", {}).get("directory")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    name_root = args.name_root or slugify_title(args.title)
    cover_title_text = args.title
    thumbnail_text = args.title_text or args.title
    subtitle = args.subtitle
    provider = resolve_provider(config, args.provider)
    dimensions = resolve_dimensions(
        config,
        args.cover_width,
        args.cover_height,
        args.thumb_width,
        args.thumb_height,
    )
    models = resolve_models(config, args.text_model, args.image_model)

    cover_path = output_dir / f"{name_root}_cover.jpg"
    thumb_path = output_dir / f"{name_root}_thumb.jpg"

    return ResolvedRequest(
        ok=True,
        title=args.title,
        synopsis=args.synopsis,
        name_root=name_root,
        output_dir=str(output_dir),
        cover_title_text=cover_title_text,
        thumbnail_text=thumbnail_text,
        subtitle=subtitle,
        config_path=str(config_path) if config_path else None,
        provider=provider,
        text_model=models["text"],
        image_model=models["image"],
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


def request_gemini_json(api_key: str, model: str, prompt: str) -> dict[str, Any]:
    """Call Gemini text generation and parse the result as JSON."""
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    response = request_gemini(api_key, model, payload)
    text = extract_text(response)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise CliError(f"Gemini returned invalid JSON for direction generation: {exc}")


def request_gemini_image(
    api_key: str,
    model: str,
    prompt: str,
    reference_image: Optional[bytes] = None,
    mime_type: str = "image/jpeg",
) -> bytes:
    """Call Gemini image generation or editing and return image bytes."""
    parts: list[dict[str, Any]] = [{"text": prompt}]
    if reference_image is not None:
        parts.append(
            {
                "inlineData": {
                    "mimeType": mime_type,
                    "data": base64.b64encode(reference_image).decode("ascii"),
                }
            }
        )

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    response = request_gemini(api_key, model, payload)
    return extract_image(response)


def request_gemini(api_key: str, model: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Perform a REST request against the Gemini API."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib.parse.quote(model, safe='')}:generateContent?key={api_key}"
    )
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise CliError(f"Gemini API request failed: {body}")
    except urllib.error.URLError as exc:
        raise CliError(f"Gemini API network error: {exc.reason}")


def extract_text(response: dict[str, Any]) -> str:
    """Extract text from a Gemini response."""
    try:
        parts = response["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError):
        raise CliError("Gemini response did not include text content")

    texts = [part.get("text") for part in parts if part.get("text")]
    if not texts:
        raise CliError("Gemini response did not include any text parts")
    return "\n".join(texts)


def extract_image(response: dict[str, Any]) -> bytes:
    """Extract the first inline image from a Gemini response."""
    try:
        parts = response["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError):
        raise CliError("Gemini response did not include content parts")

    for part in parts:
        inline = part.get("inlineData")
        if inline and inline.get("data"):
            return base64.b64decode(inline["data"])
    raise CliError("Gemini response did not include a generated image")


def build_direction_prompt(request: ResolvedRequest) -> str:
    """Build the text prompt that turns story inputs into image direction."""
    return f"""
You are the built-in story image direction engine for a Python CLI.

Your job is to turn a story title and synopsis into a reusable visual direction
and two image prompts:
1. cover_prompt
2. thumbnail_prompt

Rules:
- The cover and thumbnail must feel like the same campaign.
- The cover is the canonical cinematic image.
- The thumbnail is a stronger, more clickable edit of the same scene.
- The cover must include the exact story title text provided.
- The thumbnail must include the exact title text provided.
- The thumbnail should include the subtitle text provided when one exists.
- Keep the main subject, setting, palette, and mood consistent.
- Avoid generic filler and avoid overstuffed scenes.
- Optimize the cover for a 16:9 story/MP4 background.
- Optimize the thumbnail for a 16:9 YouTube thumbnail.
- Make the title on the cover readable, elegant, and integrated into the composition.
- Do not place giant centered text that dominates the whole cover image unless absolutely necessary.
- Put the cover title in a natural title-safe area using negative space, sky, fog, architecture, or other compositionally appropriate regions.
- Keep the main focal subject unobstructed by cover text.
- Make the thumbnail title bold, prominent, and highly readable at small size.
- Avoid oversized centered text blocks that fill the whole thumbnail unless compositionally justified.
- Place the thumbnail title in a deliberate text-safe zone with attractive hierarchy.
- If subtitle text is provided, use it as a smaller secondary line near the title with clear hierarchy and attractive placement.
- Keep title and subtitle aligned and visually intentional.

Return JSON only with this shape:
{{
  "subject": "...",
  "setting": "...",
  "mood": "...",
  "motifs": ["...", "..."],
  "palette": "...",
  "composition": "...",
  "continuity_rules": ["...", "..."],
  "cover_prompt": "...",
  "thumbnail_prompt": "..."
}}

Story title: {request.title}
Cover title text: {request.cover_title_text}
Thumbnail title text: {request.thumbnail_text}
Thumbnail subtitle text: {request.subtitle or "(none)"}
Synopsis: {request.synopsis}
""".strip()


def write_file(path: str, data: bytes) -> None:
    """Write bytes to disk, creating parent directories if needed."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)


def metadata_path_for(request: ResolvedRequest) -> Path:
    """Return the metadata sidecar path for a paired generation run."""
    return Path(request.output_dir) / f"{request.name_root}_metadata.json"


def resolve_reference_mime_type(path: str) -> str:
    """Guess the MIME type for a reference image path."""
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "image/jpeg"


def perform_generation(request: ResolvedRequest) -> GenerationResult:
    """Generate paired images through Gemini and write outputs plus metadata."""
    if request.provider != "gemini":
        raise CliError(
            f"Unsupported provider '{request.provider}'. Currently supported: gemini"
        )

    load_dotenv(Path.cwd() / ".env")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise CliError("GEMINI_API_KEY is not set")

    direction = request_gemini_json(
        api_key=api_key,
        model=request.text_model,
        prompt=build_direction_prompt(request),
    )

    cover_prompt = direction["cover_prompt"]
    thumbnail_prompt = direction["thumbnail_prompt"]

    cover_image = request_gemini_image(
        api_key=api_key,
        model=request.image_model,
        prompt=cover_prompt,
    )
    write_file(request.outputs["cover"].path, cover_image)

    thumbnail_image = request_gemini_image(
        api_key=api_key,
        model=request.image_model,
        prompt=thumbnail_prompt,
        reference_image=cover_image,
        mime_type=resolve_reference_mime_type(request.outputs["cover"].path),
    )
    write_file(request.outputs["thumbnail"].path, thumbnail_image)

    metadata_path = metadata_path_for(request)
    result = GenerationResult(
        ok=True,
        title=request.title,
        synopsis=request.synopsis,
        name_root=request.name_root,
        output_dir=request.output_dir,
        cover_title_text=request.cover_title_text,
        thumbnail_text=request.thumbnail_text,
        subtitle=request.subtitle,
        models={"text": request.text_model, "image": request.image_model},
        outputs=request.outputs,
        direction=direction,
        prompts={"cover": cover_prompt, "thumbnail": thumbnail_prompt},
        metadata_path=str(metadata_path),
    )
    metadata = RunMetadata(
        ok=True,
        provider=request.provider,
        prompt_logic_version=PROMPT_LOGIC_VERSION,
        title=request.title,
        synopsis=request.synopsis,
        name_root=request.name_root,
        output_dir=request.output_dir,
        cover_title_text=request.cover_title_text,
        thumbnail_text=request.thumbnail_text,
        subtitle=request.subtitle,
        config_path=request.config_path,
        models=result.models,
        requested_outputs=request.outputs,
        direction=direction,
        prompts=result.prompts,
        metadata_path=str(metadata_path),
    )
    metadata_path.write_text(json.dumps(asdict(metadata), indent=2) + "\n")
    return result


def cmd_generate(args: argparse.Namespace) -> int:
    """Handle the generate command."""
    request = build_resolved_request(args)

    if args.dry_run:
        print(json.dumps(asdict(request), indent=2))
        return 0

    result = perform_generation(request)
    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"Cover: {result.outputs['cover'].path}")
        print(f"Thumbnail: {result.outputs['thumbnail'].path}")
        print(f"Metadata: {result.metadata_path}")
    return 0


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
        help="Generate paired story cover and thumbnail assets.",
    )
    generate.add_argument("--title", required=True, help="Story title.")
    generate.add_argument("--synopsis", required=True, help="Story synopsis.")
    generate.add_argument(
        "--title-text",
        help="Optional thumbnail text override. Defaults to the story title.",
    )
    generate.add_argument(
        "--subtitle",
        help="Optional subtitle text to include on the thumbnail.",
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
        "--provider",
        help=f"Optional provider override. Defaults to {DEFAULT_PROVIDER}.",
    )
    generate.add_argument(
        "--text-model",
        help=f"Optional text model override. Defaults to {DEFAULT_TEXT_MODEL}.",
    )
    generate.add_argument(
        "--image-model",
        help=f"Optional image model override. Defaults to {DEFAULT_IMAGE_MODEL}.",
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
        help="Print machine-readable output.",
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
    try:
        return args.func(args)
    except CliError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": str(exc)}, indent=2), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
