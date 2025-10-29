from fastapi import APIRouter

router = APIRouter()

REGION_COORDINATES = {
    0: {"lat": 40.697559, "lon": -73.938514, "name": "Brooklyn (Lewis Ave)"},
    1: {"lat": 40.759528, "lon": -73.976445, "name": "Midtown East"},
    2: {"lat": 40.721586, "lon": -74.001703, "name": "SoHo"},
    3: {"lat": 40.645794, "lon": -73.784486, "name": "JFK Airport"},
    4: {"lat": 40.780965, "lon": -73.953164, "name": "Yorkville (Upper East Side)"},
    5: {"lat": 40.731761, "lon": -74.001188, "name": "West Village"},
    6: {"lat": 40.771788, "lon": -73.869354, "name": "LaGuardia Airport"},
    7: {"lat": 40.758815, "lon": -73.989673, "name": "Hell's Kitchen"},
    8: {"lat": 40.825608, "lon": -73.943164, "name": "Sugar Hill (Harlem)"},
    9: {"lat": 40.746008, "lon": -73.918474, "name": "Sunnyside (Queens)"},
    10: {"lat": 40.748669, "lon": -73.977354, "name": "Murray Hill"},
    11: {"lat": 40.792246, "lon": -73.970956, "name": "Upper West Side"},
    12: {"lat": 40.688296, "lon": -73.985300, "name": "Boerum Hill (Brooklyn)"},
    13: {"lat": 40.723500, "lon": -73.988594, "name": "East Village"},
    14: {"lat": 40.718261, "lon": -73.833562, "name": "Forest Hills (Queens)"},
    15: {"lat": 40.742049, "lon": -74.002639, "name": "Chelsea"},
    16: {"lat": 40.770768, "lon": -73.958114, "name": "Lenox Hill (Upper East Side)"},
    17: {"lat": 40.745609, "lon": -73.989998, "name": "NoMad"},
    18: {"lat": 40.780199, "lon": -73.979587, "name": "Upper West Side (W 75th St)"},
    19: {"lat": 40.803543, "lon": -73.953926, "name": "Harlem"},
    20: {"lat": 40.716070, "lon": -73.955385, "name": "Williamsburg (Brooklyn)"},
    21: {"lat": 40.768088, "lon": -73.984205, "name": "Columbus Circle"},
    22: {"lat": 40.764269, "lon": -73.924806, "name": "Ravenswood (Queens)"},
    23: {"lat": 40.706715, "lon": -74.010035, "name": "Financial District"},
    24: {"lat": 40.660978, "lon": -73.989492, "name": "Sunset Park (Brooklyn)"},
    25: {"lat": 40.761009, "lon": -73.966546, "name": "Sutton (Midtown East)"},
    26: {"lat": 40.751852, "lon": -73.993225, "name": "Garment District"},
    27: {"lat": 40.714820, "lon": -74.011286, "name": "Tribeca"},
    28: {"lat": 40.735326, "lon": -73.986197, "name": "Gramercy"},
    29: {"lat": 40.667323, "lon": -73.947923, "name": "Crown Heights (Brooklyn)"}
}

@router.get("/regions")
async def get_all_regions():
    return REGION_COORDINATES
