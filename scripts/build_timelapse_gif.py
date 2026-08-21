#!/usr/bin/env python3
"""Build NDVI timelapse GIF for README to assets/ndvi-timelapse.gif"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

FRAMES = [
    ("ndvi-2013.jpg", "2013"),
    ("ndvi-2020.jpg", "2020"),
    ("ndvi-2025.jpg", "2025"),
]


def labeled_frame(path: Path, year: str) -> Image.Image:
    im = Image.open(path).convert("RGB")
    im.thumbnail((900, 600), Image.Resampling.LANCZOS)
    bar = Image.new("RGB", (im.width, im.height + 36), (10, 18, 16))
    bar.paste(im, (0, 36))
    draw = ImageDraw.Draw(bar)
    draw.text((12, 8), f"Tatai Wildlife Sanctuary · NDVI · {year}", fill=(110, 207, 138))
    return bar


def main() -> None:
    frames = [labeled_frame(ASSETS / f, year) for f, year in FRAMES]
    sequence = frames + frames[-2:0:-1]
    out = ASSETS / "ndvi-timelapse.gif"
    sequence[0].save(
        out,
        save_all=True,
        append_images=sequence[1:],
        duration=900,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
