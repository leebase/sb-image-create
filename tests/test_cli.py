from __future__ import annotations

import json

from sb_image_create.main import main


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
    assert payload["thumbnail_text"] == "The Clockmaker's Debt"
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
