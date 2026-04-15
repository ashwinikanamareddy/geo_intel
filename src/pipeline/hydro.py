from __future__ import annotations

import os
import numpy as np
import rasterio

from src.config import DTM_PATH, FILLED_DTM_PATH, NODATA


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def run() -> None:
    _ensure_dir(FILLED_DTM_PATH)

    with rasterio.open(DTM_PATH) as src:
        dtm = src.read(1).astype(np.float32)
        profile = src.profile.copy()

    dtm = np.where(np.isfinite(dtm), dtm, NODATA).astype(np.float32)

    try:
        import richdem as rd

        rd_dtm = rd.rdarray(dtm, no_data=NODATA)
        rd.FillDepressions(rd_dtm, in_place=True)
        filled = np.array(rd_dtm, dtype=np.float32)
    except Exception:
        # Safe fallback if richdem is unavailable
        filled = dtm.copy()
        valid = filled[filled != NODATA]
        if valid.size > 0:
            filled[filled == NODATA] = float(np.median(valid))

    profile.update(dtype="float32", nodata=NODATA, compress="deflate")

    with rasterio.open(FILLED_DTM_PATH, "w", **profile) as dst:
        dst.write(filled.astype(np.float32), 1)

    print(f"filled_dtm.tif created: {FILLED_DTM_PATH}")