# Data

## In git (small)

| Path | Description |
|------|-------------|
| `data/processed/ndvi_stats.json` | Mean NDVI by year, summary delta |
| `data/processed/tatai_boundary.geojson` | Study area polygon (WGS84) |

Regenerate with `python scripts/compute_ndvi_stats.py` and `python scripts/export_boundary.py`.

## Local only (gitignored)

`data/raw/` — ~5.5 GB extracted from project archive:

- NDVI GeoTIFFs (2013, 2020, 2025)
- Landsat L1TP scenes
- FIRMS / fire classification rasters
- OSM road shapefiles (Geofabrik)

Keep on disk or link from README to Google Drive / Zenodo — do not commit rasters to GitHub.
