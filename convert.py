import geopandas as gpd
import rasterio
import matplotlib.pyplot as plt
import os

os.makedirs("frontend/public", exist_ok=True)

print("Converting drainage to GeoJSON...")
gdf = gpd.read_file("data/outputs/drainage.gpkg")
gdf.to_file("frontend/public/drainage.json", driver="GeoJSON")

print("Converting flood raster to PNG...")
with rasterio.open("data/outputs/flood_zones.tif") as src:
    img = src.read(1)
    bounds = src.bounds
    print(f"BOUNDS: {bounds.left}, {bounds.bottom}, {bounds.right}, {bounds.top}")

plt.imsave("frontend/public/flood.png", img, cmap='Reds')

print("Conversion complete.")
