# GeoIntel: AI-Powered Drainage & Flood Analysis System

GeoIntel is a high-performance geospatial platform designed for advanced hydrological analysis, flood risk assessment, and drainage infrastructure planning. Built with a robust Python backend and a modern React frontend, it leverages AI and LiDAR data to provide actionable insights for urban and rural planning.

## 🚀 Features

- **Automated LiDAR Processing**: Seamlessly convert and filter LiDAR data to create Digital Terrain Models (DTM).
- **Hydrological Modeling**:
  - Flow Accumulation & Stream Network extraction.
  - Watershed Delineation.
  - Slope and Aspect analysis.
- **Flood Risk Intelligence**: Predict flood-prone areas using height-above-nearest-drainage (HAND) and historical patterns.
- **Interactive Dashboard**: A glassmorphic React interface for real-time visualization of geospatial outputs.
- **Robust Pipeline**: Modular Python pipeline for processing large-scale geospatial datasets.

## 🛠️ Technology Stack

- **Backend**: FastAPI, PDAL, GDAL/OGR, NumPy, SciPy.
- **Frontend**: React.js, TailwindCSS (Premium Visuals), Lucide Icons.
- **Data Formats**: LAS/LAZ, GeoTIFF, GeoJSON, Parquet.

## 📂 Project Structure

```text
ai_drainage_system/
├── backend/            # FastAPI server and API endpoints
├── frontend/           # React dashboard and UI components
├── src/
│   ├── pipeline/       # Core geospatial processing logic (DTM, Flow, Flood)
│   ├── utils/          # File IO and raster/las utilities
├── notebooks/          # Research and experimental notebooks
├── data/               # Project data (ignored in git)
└── main.py             # Entry point for the full execution
```

## 🏗️ Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js & npm
- GIS Tools (GDAL/PDAL)

### Backend Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the FastAPI server:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the dev server:
   ```bash
   npm start
   ```

## 📊 Usage

1. Upload your LiDAR data (`.las` or `.laz`) via the dashboard.
2. Configure the processing parameters (filtering, resolution).
3. Run the automated pipeline to generate flood maps and drainage reports.
4. Export results in GeoJSON or PDF formats.

---
Developed for the IIT Hyderabad Hackathon.
