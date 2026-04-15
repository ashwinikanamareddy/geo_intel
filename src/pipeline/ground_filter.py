from __future__ import annotations

import os
import numpy as np
import laspy

from src.config import DATA_PATH, GROUND_PATH, USE_CSF, GROUND_PERCENTILE


def _ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def run() -> None:
    _ensure_dir(GROUND_PATH)

    print(f"Opening {DATA_PATH} for chunked processing...")
    
    with laspy.open(DATA_PATH) as f:
        # Create output file sharing same header
        with laspy.open(GROUND_PATH, mode="w", header=f.header) as writer:
            total_points = f.header.point_count
            points_processed = 0
            points_kept = 0
            
            chunk_size = 1_000_000
            for chunk in f.chunk_iterator(chunk_size):
                z = np.asarray(chunk.z)
                
                # Local percentile per chunk for extreme memory efficiency
                threshold = np.percentile(z, GROUND_PERCENTILE)
                ground_mask = z <= threshold
                
                writer.write_points(chunk[ground_mask])
                
                points_processed += len(chunk)
                points_kept += np.sum(ground_mask)
                print(f"Processed ground filter chunk: {points_processed}/{total_points}...")
                
    print(f"ground.las created: {GROUND_PATH}")
    print(f"Ground points kept: {points_kept} / {total_points}")