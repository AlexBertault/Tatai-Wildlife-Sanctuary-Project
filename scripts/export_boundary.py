#!/usr/bin/env python3
"""Export study boundary → data/processed/tatai_boundary.geojson"""

from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import rasterio
from shapely.geometry import box

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed"
OUT.mkdir(parents=True, exist_ok=True)

WDPA = ROOT / "data/raw/Data/WDPA_WDOECM_Mar2026_Public_555703469_shp-polygons.shp"
NDVI = ROOT / "data/raw/Data/NDVI/NDVI_2013_output.tif"


def from_wdpa() -> gpd.GeoDataFrame | None:
    if not WDPA.exists():
        return None
    try:
        gdf = gpd.read_file(WDPA)
    except Exception:
        import os

        os.environ["SHAPE_RESTORE_SHX"] = "YES"
        gdf = gpd.read_file(WDPA)
    for col in gdf.columns:
        if "NAME" in col.upper():
            mask = gdf[col].astype(str).str.contains("Tatai", case=False, na=False)
            if mask.any():
                return gdf[mask].to_crs("EPSG:4326")
    return None


def from_raster_extent() -> gpd.GeoDataFrame:
    with rasterio.open(NDVI) as src:
        b = src.bounds
        return gpd.GeoDataFrame(
            {"name": ["Tatai Wildlife Sanctuary (NDVI extent)"]},
            geometry=[box(b.left, b.bottom, b.right, b.top)],
            crs=src.crs,
        ).to_crs("EPSG:4326")


def main() -> None:
    gdf = from_wdpa() or from_raster_extent()
    out = OUT / "tatai_boundary.geojson"
    gdf.to_file(out, driver="GeoJSON")
    print(f"Wrote {out} ({len(gdf)} feature(s))")


if __name__ == "__main__":
    main()
