import React, { useState } from "react";
import "./App.css";

function App() {
  const [status, setStatus] = useState("idle"); // idle, processing, completed
  const [file, setFile] = useState(null);
  
  // Fake progress steps simulation for the UI
  const [currentStep, setCurrentStep] = useState(0);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setStatus("processing");
    setCurrentStep(0);
    
    // Simulate steps purely for UI logic while the real pipeline runs
    const stepInterval = setInterval(() => {
      setCurrentStep(prev => prev < 4 ? prev + 1 : prev);
    }, 1500);

    const formData = new FormData();
    formData.append("file", file);

    try {
      await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });
      clearInterval(stepInterval);
      setCurrentStep(4);
      setTimeout(() => setStatus("completed"), 500);
    } catch (err) {
      console.error(err);
      alert("Pipeline failed or server unreachable.");
      clearInterval(stepInterval);
      setStatus("idle");
    }
  };

  const resetBase = () => {
    setStatus("idle");
    setFile(null);
    setCurrentStep(0);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-text">
          <h1>AI Drainage Intelligence System</h1>
          <p>LiDAR-based Flood & Drainage Analysis</p>
        </div>
        <div>
          {status === "idle" && <span className="status-badge status-idle">⚫ Idle</span>}
          {status === "processing" && <span className="status-badge status-processing">🔵 Processing...</span>}
          {status === "completed" && <span className="status-badge status-completed">🟢 Completed</span>}
        </div>
      </header>

      {/* Main Content */}
      <main>
        {status === "idle" && (
          <div className="hero-card fade-in">
            <h2>Upload LiDAR (.LAS) file</h2>
            <p style={{ color: "var(--text-light)", marginBottom: "30px" }}>Secure, fast, and scalable analytical processing</p>
            
            <div className="upload-box">
              <input type="file" className="file-input" onChange={handleFileChange} accept=".las,.laz" />
              <div style={{ fontSize: "40px", marginBottom: "15px" }}>📁</div>
              {file ? (
                <div>
                  <strong>{file.name}</strong>
                  <p style={{ margin: "5px 0 0" }}>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              ) : (
                <p>Drag & drop your file here, or click to browse</p>
              )}
            </div>

            {file && (
              <button className="btn-primary" onClick={handleUpload}>
                Run AI Pipeline
              </button>
            )}
          </div>
        )}

        {status === "processing" && (
          <div className="hero-card fade-in">
            <div className="spinner"></div>
            <h2>Processing terrain data…</h2>
            
            <div className="processing-container">
              <div className={`step-item ${currentStep === 0 ? 'step-active' : (currentStep > 0 ? 'step-done' : '')}`}>
                {currentStep > 0 ? '✔' : '⏳'} Ground Filtering
              </div>
              <div className={`step-item ${currentStep === 1 ? 'step-active' : (currentStep > 1 ? 'step-done' : '')}`}>
                {currentStep > 1 ? '✔' : '⏳'} DTM Generation
              </div>
              <div className={`step-item ${currentStep === 2 ? 'step-active' : (currentStep > 2 ? 'step-done' : '')}`}>
                {currentStep > 2 ? '✔' : '⏳'} Flow Analysis
              </div>
              <div className={`step-item ${currentStep === 3 ? 'step-active' : (currentStep > 3 ? 'step-done' : '')}`}>
                {currentStep > 3 ? '✔' : '⏳'} Flood Detection
              </div>
            </div>
          </div>
        )}

        {status === "completed" && (
          <div className="fade-in">
            <div className="results-grid">
              
              <div className="result-card">
                <div className="result-img-wrapper overlay-red">
                  <img src="http://127.0.0.1:8000/outputs/flood_zones.png" alt="Flood Map" />
                </div>
                <div className="card-label">🚨 Flood Risk Zones</div>
              </div>

              <div className="result-card">
                <div className="result-img-wrapper">
                  <img src="http://127.0.0.1:8000/outputs/slope.png" alt="Slope Map" />
                </div>
                <div className="card-label">⛰️ Terrain Slope</div>
              </div>

              <div className="result-card">
                <div className="result-img-wrapper">
                  <img src="http://127.0.0.1:8000/outputs/flow_acc.png" alt="Flow Map" />
                </div>
                <div className="card-label">💧 Water Flow Paths</div>
              </div>

              <div className="result-card">
                <div className="result-img-wrapper">
                  {/* Using an alternative hue rotated view for Drainage Extraction if image is missing */}
                  <img src="http://127.0.0.1:8000/outputs/flow_acc.png" alt="Drainage Extent" style={{ filter: 'hue-rotate(180deg)' }} />
                </div>
                <div className="card-label">🗺️ Drainage Extraction</div>
              </div>

            </div>

            <div className="action-buttons">
              <button className="btn-outline">Download Results</button>
              <button className="btn-outline">View in GIS</button>
              <button className="btn-primary" style={{ margin: 0 }} onClick={resetBase}>Run Again</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
