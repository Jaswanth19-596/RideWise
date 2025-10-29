from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from backend.models.predictor import predictor
from datetime import datetime # Import datetime for ISO formatting

router = APIRouter()

class PredictionResponse(BaseModel):
    region_id: int
    predicted_pickups: float
    features: Dict[str, bool]

class AllRegionsResponse(BaseModel):
    timestamp: str
    predictions: List[PredictionResponse]

@router.get("/predict/{region_id}", response_model=PredictionResponse)
async def predict_region(region_id: int):
    """Predict demand for a specific region"""
    try:
        result = predictor.predict(region_id) 
        
        return {
            "region_id": region_id,
            "predicted_pickups": result["prediction"],
            "features": result["features"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error for region {region_id}: {e}")

@router.get("/predict-all", response_model=AllRegionsResponse)
async def predict_all_regions():
    """Predict demand for all regions"""
    try:
        current_time = predictor.get_simulation_time()
        predictions_list = []
        
        # NOTE: You should define the range of regions based on your dataset (e.g., range(1, 266))
        for region_id in range(1, 26): 
            try:
                result = predictor.predict(region_id)
                
                predictions_list.append({
                    "region_id": region_id,
                    "predicted_pickups": result["prediction"],
                    "features": result["features"],
                })
            except ValueError as e:
                # Catch specific data errors and log, but continue to next region
                print(f"Skipping prediction for region {region_id} due to data error: {e}")
                continue
            except Exception as e:
                # Catch general prediction errors
                print(f"Unexpected error predicting for region {region_id}: {e}")
                continue
        
        return {
            "timestamp": current_time.isoformat(),
            "predictions": predictions_list,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))