from fastapi import APIRouter

router = APIRouter()

# Region coordinates - adjust based on your actual data
REGION_COORDINATES = {
    1: {"lat": 40.7589, "lon": -73.9851, "name": "Midtown"},
    2: {"lat": 40.7614, "lon": -73.9776, "name": "Upper East Side"},
    3: {"lat": 40.7580, "lon": -73.9855, "name": "Times Square"},
    4: {"lat": 40.7505, "lon": -73.9934, "name": "Chelsea"},
    5: {"lat": 40.7489, "lon": -73.9680, "name": "East Village"},
    6: {"lat": 40.7614, "lon": -73.9776, "name": "Upper West Side"},
    7: {"lat": 40.7505, "lon": -73.9934, "name": "Hell's Kitchen"},
    8: {"lat": 40.7489, "lon": -73.9680, "name": "Lower Manhattan"}
}

@router.get("/regions")
async def get_regions():
    """Get all available regions with coordinates"""
    return REGION_COORDINATES

@router.get("/regions/{region_id}")
async def get_region(region_id: int):
    """Get specific region information"""
    if region_id not in REGION_COORDINATES:
        raise HTTPException(status_code=404, detail="Region not found")
    return REGION_COORDINATES[region_id]

@router.get("/current-time")
async def get_current_time():
    """Get current simulation time"""
    from backend.models.predictor import predictor
    return {
        "timestamp": predictor.get_simulation_time().isoformat(),
        "real_time": datetime.now().isoformat()
    }