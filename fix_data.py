import geopandas as gpd
from shapely.affinity import translate, scale

gdf = gpd.read_file("frontend/public/drainage.json")

# Current bounds are roughly 0 to 100 for x and y
# Target India bounds: lon (78.12 to 78.30), lat (15.45 to 15.60)
# lon scale = (78.30 - 78.12) / 100 = 0.0018
# lat scale = (15.60 - 15.45) / 100 = 0.0015
# x_off = 78.12, y_off = 15.45

gdf.geometry = gdf.geometry.apply(lambda geom: scale(geom, xfact=0.0018, yfact=0.0015, origin=(0, 0)))
gdf.geometry = gdf.geometry.apply(lambda geom: translate(geom, xoff=78.12, yoff=15.45))

gdf.to_file("frontend/public/drainage.json", driver="GeoJSON")
print("Fixed drainage.json")
