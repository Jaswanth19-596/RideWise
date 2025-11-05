from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Tuple, Optional
from classes.predictor import predictor
import joblib
from routers.regions import REGION_COORDINATES_NAMES, REGION_COORDINATES
from utils.haversine import haversine_distance
from pathlib import Path
import logging
from functools import lru_cache
from datetime import datetime
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_PATH = PROJECT_ROOT / 'models'
MAX_REGIONS = 30

router = APIRouter()


class PredictionResponse(BaseModel):
    region_id: int
    predicted_pickups: float
    features: Dict[str, bool]
    distance: Optional[float] = None


class AllRegionsResponse(BaseModel):
    predictions: List[PredictionResponse]
    timestamp: Optional[str] = None


# @lru_cache(maxsize=1)
def load_models() -> Tuple:
    try:
        kmeans = joblib.load(MODELS_PATH / 'kmeans.joblib')
        scaler = joblib.load(MODELS_PATH / 'scaler.joblib')
    
        return kmeans, scaler
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Model files not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load models: {e}")


def get_neighboring_regions(region_id: int, n_neighbors: int) -> Tuple[List[int], List[float]]:
    if region_id not in REGION_COORDINATES_NAMES:
        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    
    region = REGION_COORDINATES_NAMES[region_id]
    lat, lon = region['lat'], region['lon']
    
    _, scaler = load_models()
    center_coordinates = scaler.transform(REGION_COORDINATES)

    distances = []
    for idx, (neighbor_lat, neighbor_long) in enumerate(scaler.inverse_transform(center_coordinates)):
        dist = haversine_distance(neighbor_lat, neighbor_long, lat, lon)
        distances.append((idx, dist))
    
    sorted_distances = sorted(distances, key=lambda x: x[1])[:n_neighbors]

    neighbors = [idx for idx, _ in sorted_distances]
    neighbor_distances = [dist for _, dist in sorted_distances]

    return neighbors, neighbor_distances


@router.get("/predict/{region_id}", response_model=AllRegionsResponse)
async def predict_region(region_id: int):
    try:
        neighbor_regions, distances = get_neighboring_regions(region_id, 8)
        predictions = []
        
        for idx, region in enumerate(neighbor_regions):
            try:
                result = predictor.predict(int(region))
                predictions.append(PredictionResponse(
                    region_id=int(region),
                    predicted_pickups=result["prediction"],
                    features=result["features"],
                    distance=distances[idx],
                ))
            except Exception as e:
                logger.warning(f"Failed prediction for region {region}: {e}")
        
        if not predictions:
            raise HTTPException(status_code=500, detail="No predictions generated")
        
        return AllRegionsResponse(predictions=predictions, timestamp=datetime.utcnow().isoformat())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting region {region_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predict-all/", response_model=AllRegionsResponse)
async def predict_all_regions():
    try:
        predictions = []
        # For every region, find the demand at that point of time
        for idx, region in enumerate(range(0, 30)):
            try:
                result = predictor.predict(int(region))
                predictions.append(PredictionResponse(
                    region_id=int(region),
                    predicted_pickups=result["prediction"],
                    features=result["features"],
                ))
            except Exception as e:
                logger.warning(e)
                logger.warning(f"Failed prediction for region {region}: {e}")
        
        if not predictions:
            raise HTTPException(status_code=500, detail="No predictions generated")
        
        return AllRegionsResponse(predictions=predictions, timestamp=datetime.utcnow().isoformat())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error predicting region : {e}")
        raise HTTPException(status_code=500, detail=str(e))