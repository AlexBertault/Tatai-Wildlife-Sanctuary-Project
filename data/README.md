# Data

## Tracked in git

| Path | What it is |
|------|------------|
| `data/processed/ndvi_stats.json` | Mean NDVI by year plus summary delta |
| `data/processed/tatai_boundary.geojson` | Study area polygon (WGS84) |

Rebuild with:

```bash
python scripts/compute_ndvi_stats.py
python scripts/export_boundary.py
```

## Local only (gitignored)

`data/raw/` is about 5.5 GB from the project archive:

- NDVI GeoTIFFs (2013, 2020, 2025)
- Landsat L1TP scenes
- FIRMS / fire classification rasters
- OSM road shapefiles (Geofabrik)

Keep it on disk. Do not push rasters to GitHub.
