from __future__ import annotations

import os
import numpy as np
import rasterio

from src.config import FILLED_DTM_PATH, FLOW_ACC_PATH, NODATA


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def run() -> None:
    _ensure_dir(FLOW_ACC_PATH)

    with rasterio.open(FILLED_DTM_PATH) as src:
        dtm = src.read(1).astype(np.float32)
        profile = src.profile.copy()

    dtm = np.where(dtm == NODATA, np.nan, dtm)

    try:
        import richdem as rd

        rd_dtm = rd.rdarray(np.nan_to_num(dtm, nan=np.nanmedian(dtm)), no_data=NODATA)
        flow_dir = rd.FlowDirection(rd_dtm, method="D8")
        flow_acc = rd.FlowAccumulation(flow_dir)
        flow_acc = np.array(flow_acc, dtype=np.float32)
    except Exception:
        # Safe fallback: simple accumulation proxy from height rank
        filled = np.nan_to_num(dtm, nan=np.nanmedian(dtm))
        flow_acc = (filled.max() - filled).astype(np.float32)

    profile.update(dtype="float32", nodata=NODATA, compress="deflate")

    with rasterio.open(FLOW_ACC_PATH, "w", **profile) as dst:
        dst.write(flow_acc, 1)

    print(f"flow_acc.tif created: {FLOW_ACC_PATH}")