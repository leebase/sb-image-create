from __future__ import annotations

import json
from pathlib import Path

from sb_image_create.main import build_direction_prompt, build_resolved_request, main


def test_generate_uses_slugged_title_and_cwd(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = main(
        [
            "generate",
            "--title",
            "The Clockmaker's Debt",
            "--synopsis",
            "A desperate watchmaker chases stolen years.",
            "--dry-run",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["name_root"] == "the-clockmaker-s-debt"
    assert payload["cover_title_text"] == "The Clockmaker's Debt"
    assert payload["thumbnail_text"] == "The Clockmaker's Debt"
    assert payload["subtitle"] is None
    assert payload["outputs"]["cover"]["path"].endswith(
        "the-clockmaker-s-debt_cover.jpg"
    )
    assert payload["outputs"]["thumbnail"]["path"].endswith(
        "the-clockmaker-s-debt_thumb.jpg"
    )


def test_generate_allows_config_and_cli_overrides(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "image-config.toml"
    config_path.write_text(
        """
[output]
directory = "assets"

[images.cover]
width = 2000
height = 1000

[images.thumbnail]
width = 1400
height = 800
""".strip()
    )

    exit_code = main(
        [
            "generate",
            "--title",
            "Moon Harbor",
            "--synopsis",
            "A diver searches a flooded observatory.",
            "--cover-width",
            "2500",
            "--dry-run",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["output_dir"].endswith("assets")
    assert payload["outputs"]["cover"]["width"] == 2500
    assert payload["outputs"]["cover"]["height"] == 1000
    assert payload["outputs"]["thumbnail"]["width"] == 1400
    assert payload["outputs"]["thumbnail"]["height"] == 800


def test_generate_writes_paired_outputs_and_metadata(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    direction = {
        "subject": "A lone archivist",
        "setting": "A ruined library under moonlight",
        "mood": "haunting",
        "motifs": ["dust", "silver light"],
        "palette": "blue and silver",
        "composition": "wide cinematic frame",
        "continuity_rules": ["keep the same central figure"],
        "cover_prompt": "cover prompt",
        "thumbnail_prompt": "thumbnail prompt",
    }
    image_bytes = b"fake-jpeg-data"

    monkeypatch.setattr(
        "sb_image_create.main.request_gemini_json",
        lambda api_key, model, prompt: direction,
    )
    monkeypatch.setattr(
        "sb_image_create.main.request_gemini_image",
        lambda api_key, model, prompt, reference_image=None, mime_type="image/jpeg": image_bytes,
    )

    exit_code = main(
        [
            "generate",
            "--title",
            "Archive of Salt",
            "--synopsis",
            "An archivist protects the last wet paper maps in a drowned empire.",
            "--subtitle",
            "The maps must survive the flood.",
            "--output-dir",
            str(tmp_path),
            "--json",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    cover_path = Path(payload["outputs"]["cover"]["path"])
    thumb_path = Path(payload["outputs"]["thumbnail"]["path"])
    metadata_path = Path(payload["metadata_path"])

    assert cover_path.exists()
    assert thumb_path.exists()
    assert metadata_path.exists()
    assert cover_path.read_bytes() == image_bytes
    assert thumb_path.read_bytes() == image_bytes

    metadata = json.loads(metadata_path.read_text())
    assert metadata["provider"] == "gemini"
    assert metadata["prompt_logic_version"] == "v2"
    assert metadata["cover_title_text"] == "Archive of Salt"
    assert metadata["thumbnail_text"] == "Archive of Salt"
    assert metadata["subtitle"] == "The maps must survive the flood."
    assert metadata["requested_outputs"]["cover"]["path"] == str(cover_path)
    assert metadata["requested_outputs"]["thumbnail"]["path"] == str(thumb_path)


def test_generate_dry_run_accepts_subtitle(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    exit_code = main(
        [
            "generate",
            "--title",
            "Signal Bloom",
            "--synopsis",
            "A radio tower starts flowering with impossible frequencies.",
            "--subtitle",
            "The last station starts to sing.",
            "--dry-run",
        ]
    )

    assert exit_code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["cover_title_text"] == "Signal Bloom"
    assert payload["thumbnail_text"] == "Signal Bloom"
    assert payload["subtitle"] == "The last station starts to sing."


def test_generate_rejects_unsupported_provider(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")

    exit_code = main(
        [
            "generate",
            "--title",
            "Signal Bloom",
            "--synopsis",
            "A radio tower starts flowering with impossible frequencies.",
            "--provider",
            "openrouter",
            "--json",
        ]
    )

    assert exit_code == 1
    payload = json.loads(capsys.readouterr().err)
    assert payload["ok"] is False
    assert "Unsupported provider" in payload["error"]


def test_direction_prompt_demands_text_hierarchy_and_placement(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    request = build_resolved_request(
        type(
            "Args",
            (),
            {
                "title": "The Lord of the Rings",
                "synopsis": "A hobbit bears a ring toward doom.",
                "title_text": None,
                "subtitle": "One ring. One journey. One last chance.",
                "name_root": None,
                "output_dir": None,
                "provider": None,
                "cover_width": None,
                "cover_height": None,
                "thumb_width": None,
                "thumb_height": None,
                "text_model": None,
                "image_model": None,
                "config": "image-config.toml",
            },
        )()
    )

    prompt = build_direction_prompt(request)
    assert "Do not place giant centered text" in prompt
    assert "Keep the main focal subject unobstructed" in prompt
    assert "smaller secondary line" in prompt
    assert "Thumbnail subtitle text: One ring. One journey. One last chance." in prompt
