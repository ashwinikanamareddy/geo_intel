DATA_PATH = "data/raw/input.las"

GROUND_PATH = "data/interim/ground.las"
DTM_PATH = "data/interim/dtm.tif"
FILLED_DTM_PATH = "data/interim/filled_dtm.tif"

SLOPE_PATH = "data/interim/slope.tif"
FLOW_ACC_PATH = "data/interim/flow_acc.tif"

FLOOD_PATH = "data/outputs/flood_zones.tif"
DRAINAGE_PATH = "data/outputs/drainage.gpkg"
WATERSHED_PATH = "data/outputs/watershed.gpkg"

RESOLUTION = 1.0
FLOW_THRESHOLD = 1000

# Ground filtering
USE_CSF = False
GROUND_PERCENTILE = 60

# DTM / hydrology
NODATA = -9999.0