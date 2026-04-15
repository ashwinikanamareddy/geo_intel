from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import subprocess
import rasterio
import matplotlib.pyplot as plt
import os

app = FastAPI()

# Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/outputs/viz", exist_ok=True)

UPLOAD_PATH = "data/raw/input.las"

def tif_to_png(tif_path, png_path, cmap='viridis'):
    try:
        if os.path.exists(tif_path):
            with rasterio.open(tif_path) as src:
                img = src.read(1)
            plt.imsave(png_path, img, cmap=cmap)
    except Exception as e:
        print(f"Error converting {tif_path}: {e}")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save uploaded file
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run the processing pipeline
    # The process executes main.py in the root directory
    subprocess.run(["python", "main.py"], cwd=".")

    # Convert .tif outputs to .png so the browser can easily display them
    tif_to_png("data/outputs/flood_zones.tif", "data/outputs/viz/flood_zones.png", cmap="Reds")
    tif_to_png("data/interim/slope.tif", "data/outputs/viz/slope.png", cmap="plasma")
    tif_to_png("data/interim/flow_acc.tif", "data/outputs/viz/flow_acc.png", cmap="Blues")

    return {"message": "Processing completed"}

# Serve the png visualizations over the outputs URL
app.mount("/outputs", StaticFiles(directory="data/outputs/viz"), name="outputs")
