from __future__ import annotations

import os
import numpy as np
import rasterio
from scipy.ndimage import sobel

from src.config import FILLED_DTM_PATH, SLOPE_PATH, NODATA


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def run() -> None:
    _ensure_dir(SLOPE_PATH)

    with rasterio.open(FILLED_DTM_PATH) as src:
        dtm = src.read(1).astype(np.float32)
        profile = src.profile.copy()
        res_x = src.transform.a
        res_y = abs(src.transform.e)

    dtm = np.where(dtm == NODATA, np.nan, dtm)
    dtm = np.nan_to_num(dtm, nan=np.nanmedian(dtm))

    dzdx = sobel(dtm, axis=1) / (8.0 * res_x)
    dzdy = sobel(dtm, axis=0) / (8.0 * res_y)

    slope = np.degrees(np.arctan(np.sqrt(dzdx**2 + dzdy**2))).astype(np.float32)

    profile.update(dtype="float32", nodata=NODATA, compress="deflate")

    with rasterio.open(SLOPE_PATH, "w", **profile) as dst:
        dst.write(slope, 1)

    print(f"slope.tif created: {SLOPE_PATH}")