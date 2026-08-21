-- Spatial analysis queries (PostGIS-style)
-- Illustrates zonal NDVI workflow for Tatai Wildlife Sanctuary

-- Mean NDVI by epoch (precomputed values from scripts/compute_ndvi_stats.py)
-- 2013: 0.4029 | 2020: 0.3982 | 2025: 0.3972 | delta: -0.0057

-- Zonal mean NDVI clipped to sanctuary boundary
SELECT
  z.name AS zone,
  AVG(r.ndvi) AS mean_ndvi,
  ST_Area(ST_Intersection(r.rast_geom, z.geom)) / 1e4 AS overlap_ha
FROM ndvi_raster r
JOIN tatai_boundary z ON ST_Intersects(r.rast_geom, z.geom)
WHERE r.observation_year = 2025
GROUP BY z.name;

-- Fire alerts within sanctuary (FIRMS points)
SELECT
  f.alert_date,
  f.confidence,
  ST_AsText(f.geom) AS location
FROM firms_alerts f
JOIN tatai_boundary b ON ST_Within(f.geom, b.geom)
WHERE f.alert_date BETWEEN '2015-01-01' AND '2025-12-31'
ORDER BY f.alert_date;

-- Road expansion buffer overlap with NDVI loss pixels
SELECT
  COUNT(*) AS loss_pixels_near_new_roads
FROM ndvi_change c
JOIN roads_2025 r ON ST_DWithin(c.geom, r.geom, 500)  -- 500 m buffer
WHERE c.ndvi_delta < -0.05
  AND NOT EXISTS (
    SELECT 1 FROM roads_2020 r0
    WHERE ST_DWithin(c.geom, r0.geom, 500)
  );
