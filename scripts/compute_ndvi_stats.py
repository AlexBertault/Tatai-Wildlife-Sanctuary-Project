#!/usr/bin/env python3
"""Compute NDVI summary stats from GeoTIFFs → data/processed/ndvi_stats.json"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/Data/NDVI"
OUT = ROOT / "data/processed"
OUT.mkdir(parents=True, exist_ok=True)

NDVI_FILES = {
    2013: RAW / "NDVI_2013_output.tif",
    2020: RAW / "NDVI_2020_output.tif",
    2025: RAW / "NDVI_2025_output2.tif",
}


def main() -> None:
    series = []
    for year, path in sorted(NDVI_FILES.items()):
        if not path.exists():
            raise FileNotFoundError(path)
        with rasterio.open(path) as src:
            data = src.read(1, masked=True).astype("float32")
            valid = data.compressed()
            valid = valid[~np.isnan(valid)]
            valid = valid[(valid > -1) & (valid < 1)]
        series.append(
            {
                "year": year,
                "mean": round(float(valid.mean()), 4),
                "std": round(float(valid.std()), 4),
                "min": round(float(valid.min()), 4),
                "max": round(float(valid.max()), 4),
                "pct_healthy_gt_0_5": round(float((valid > 0.5).mean() * 100), 1),
            }
        )

    payload = {
        "series": series,
        "summary": {
            "delta_2013_2025": round(series[-1]["mean"] - series[0]["mean"], 4),
            "area_ha": 144539,
            "landsat": "8/9 Collection 2 Level-1",
            "dry_season_months": ["2013-12", "2020-12", "2025-12"],
        },
    }
    out_path = OUT / "ndvi_stats.json"
    out_path.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
