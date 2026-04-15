import os
import numpy as np
import rasterio
import geopandas as gpd
from shapely.geometry import LineString
from src.config import FLOW_ACC_PATH, DRAINAGE_PATH, NODATA

def run():
    os.makedirs(os.path.dirname(DRAINAGE_PATH), exist_ok=True)

    with rasterio.open(FLOW_ACC_PATH) as src:
        flow = src.read(1).astype(np.float32)
        transform = src.transform
        crs = src.crs

    flow = np.where(flow == NODATA, np.nan, flow)
    valid = flow[np.isfinite(flow)]
    if valid.size == 0:
        raise ValueError("No valid flow accumulation values found.")

    threshold = np.percentile(valid, 95)
    mask = flow >= threshold

    rows, cols = flow.shape
    lines = []

    # Connect each high-flow cell to the nearest high-flow neighbor
    for i in range(rows):
        for j in range(cols):
            if not mask[i, j]:
                continue

            neighbors = []
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and mask[ni, nj]:
                        neighbors.append((flow[ni, nj], ni, nj))

            if not neighbors:
                continue

            # choose the strongest connected neighbor
            _, ni, nj = max(neighbors, key=lambda x: x[0])

            x1, y1 = transform * (j + 0.5, i + 0.5)
            x2, y2 = transform * (nj + 0.5, ni + 0.5)
            lines.append(LineString([(x1, y1), (x2, y2)]))

    if not lines:
        raise ValueError("No drainage lines could be extracted. Try lowering the threshold.")

    gdf = gpd.GeoDataFrame({"id": range(len(lines))}, geometry=lines, crs=crs)
    gdf.to_file(DRAINAGE_PATH, driver="GPKG")

    print("drainage.gpkg created")