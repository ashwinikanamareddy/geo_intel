import os
import numpy as np
import rasterio
import geopandas as gpd
from shapely.geometry import Polygon
from src.config import FLOW_ACC_PATH, WATERSHED_PATH, NODATA

def run():
    os.makedirs(os.path.dirname(WATERSHED_PATH), exist_ok=True)

    with rasterio.open(FLOW_ACC_PATH) as src:
        flow = src.read(1).astype(np.float32)
        transform = src.transform
        crs = src.crs

    flow = np.where(flow == NODATA, np.nan, flow)
    valid = flow[np.isfinite(flow)]
    if valid.size == 0:
        raise ValueError("No valid flow accumulation values found.")

    threshold = np.percentile(valid, 85)
    mask = flow >= threshold

    rows, cols = mask.shape
    polys = []

    for i in range(rows):
        for j in range(cols):
            if not mask[i, j]:
                continue

            x1, y1 = transform * (j, i)
            x2, y2 = transform * (j + 1, i + 1)

            poly = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
            polys.append(poly)

    if not polys:
        raise ValueError("No watershed areas could be extracted. Try lowering the threshold.")

    gdf = gpd.GeoDataFrame({"id": range(len(polys))}, geometry=polys, crs=crs)
    gdf.to_file(WATERSHED_PATH, driver="GPKG")

    print("watershed.gpkg created")