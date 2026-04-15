from __future__ import annotations

import os
import numpy as np
import laspy
import rasterio
from rasterio.transform import from_origin

from src.config import GROUND_PATH, DTM_PATH, RESOLUTION, NODATA


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _fill_nans(grid: np.ndarray) -> np.ndarray:
    valid = grid[np.isfinite(grid)]
    if valid.size == 0:
        raise ValueError("No valid ground points found to build DTM.")
    fill_value = float(np.median(valid))
    return np.where(np.isfinite(grid), grid, fill_value)


def run() -> None:
    _ensure_dir(DTM_PATH)

    with laspy.open(GROUND_PATH) as f:
        # Get bounding box efficiently without reading geometry
        min_x = f.header.x_min
        max_x = f.header.x_max
        min_y = f.header.y_min
        max_y = f.header.y_max

        cols = int(np.ceil((max_x - min_x) / RESOLUTION)) + 1
        rows = int(np.ceil((max_y - min_y) / RESOLUTION)) + 1

        grid = np.full((rows, cols), np.nan, dtype=np.float32)
        total_points = f.header.point_count
        points_processed = 0
        
        print(f"Generating DTM grid shape ({rows}, {cols})...")

        for chunk in f.chunk_iterator(1_000_000):
            x = np.asarray(chunk.x)
            y = np.asarray(chunk.y)
            z = np.asarray(chunk.z)

            col_idx = np.floor((x - min_x) / RESOLUTION).astype(int)
            row_idx = np.floor((max_y - y) / RESOLUTION).astype(int)

            # Ensure we clip bounds safely
            valid_mask = (row_idx >= 0) & (row_idx < rows) & (col_idx >= 0) & (col_idx < cols)
            r_valid = row_idx[valid_mask]
            c_valid = col_idx[valid_mask]
            z_valid = z[valid_mask]

            # Place chunks iteratively into minimal memory grid
            for r, c, elev in zip(r_valid, c_valid, z_valid):
                current = grid[r, c]
                if np.isnan(current) or elev < current:
                    grid[r, c] = elev
                    
            points_processed += len(chunk)
            print(f"Placed {points_processed}/{total_points} coordinates into grid...")

    grid = _fill_nans(grid).astype(np.float32)

    transform = from_origin(min_x, max_y, RESOLUTION, RESOLUTION)
    profile = {
        "driver": "GTiff",
        "height": grid.shape[0],
        "width": grid.shape[1],
        "count": 1,
        "dtype": "float32",
        "crs": "EPSG:4326",
        "transform": transform,
        "nodata": NODATA,
        "compress": "deflate",
    }

    with rasterio.open(DTM_PATH, "w", **profile) as dst:
        dst.write(grid, 1)

    print(f"dtm.tif created: {DTM_PATH}")