import os
import numpy as np
import rasterio
from src.config import FLOW_ACC_PATH, SLOPE_PATH, FLOOD_PATH, NODATA

def run():
    os.makedirs(os.path.dirname(FLOOD_PATH), exist_ok=True)

    with rasterio.open(FLOW_ACC_PATH) as f:
        flow = f.read(1).astype(np.float32)
        profile = f.profile.copy()

    with rasterio.open(SLOPE_PATH) as s:
        slope = s.read(1).astype(np.float32)

    flow = np.where(flow == NODATA, np.nan, flow)
    slope = np.where(slope == NODATA, np.nan, slope)

    valid_flow = flow[np.isfinite(flow)]
    if valid_flow.size == 0:
        raise ValueError("No valid flow accumulation values found.")

    flow_thresh = np.percentile(valid_flow, 90)

    # High flow + low slope = flood-prone
    flood = ((flow > flow_thresh) & (slope < 5)).astype(np.uint8)

    profile.update(dtype="uint8", count=1, nodata=0, compress="deflate")

    with rasterio.open(FLOOD_PATH, "w", **profile) as dst:
        dst.write(flood, 1)

    print("flood_zones.tif created")