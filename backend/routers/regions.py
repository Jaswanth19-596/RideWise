from fastapi import APIRouter
import mlflow

router = APIRouter()

REGION_COORDINATES_NAMES = {
    0: {"lat": 40.6911, "lon": -73.9351, "name": "Jesse Owens Playground"},
    1: {"lat": 40.7628, "lon": -73.9806, "name": "Newyork Hilton Midtown"},
    2: {"lat": 40.721586, "lon": -74.001703, "name": "Lower Manhattan"},
    3: {"lat": 40.645794, "lon": -73.784486, "name": "JFK Airport"},
    4: {"lat": 40.7838, "lon": -73.9521, "name": "Carnegie Hill"},
    5: {"lat": 40.7325, "lon": -74.002, "name": "Greenwich Village"},
    6: {"lat": 40.771788, "lon": -73.869354, "name": "LaGuardia Airport"},
    7: {"lat": 40.7588, "lon": -73.9914, "name": "Hell's Kitchen"},
    8: {"lat": 40.8293, "lon": -73.941, "name": "Upper Manhattan"},
    9: {"lat": 40.7474, "lon": -73.9398, "name": "Sculpture Center"},
    10: {"lat": 40.7531, "lon": -73.976, "name": "Grand Central"},
    11: {"lat": 40.7841, "lon": -73.9768, "name": "Upper West Side"},
    12: {"lat": 40.687, "lon": -73.9852, "name": "Boerum Hill (Brooklyn)"},
    13: {"lat": 40.7241, "lon": -73.9881, "name": "Ukranian Village"},
    14: {"lat": 40.7246, "lon": -73.847, "name": "Forest Hills (Queens)"},
    15: {"lat": 40.743, "lon": -74.0013, "name": "Chelsea"},
    16: {"lat": 40.7688, "lon": -73.9596, "name": "Lenox Hill (Upper East Side)"},
    17: {"lat": 40.7439, "lon": -73.982, "name": "Kips Bay"},
    18: {"lat": 40.7951, "lon": -73.9689, "name": "Manhattan Valley"},
    19: {"lat": 40.8084, "lon": -73.9583, "name": "Morningside Heights"},
    20: {"lat": 40.7151, "lon": -73.9549, "name": "Williamsburg (Brooklyn)"},
    21: {"lat": 40.7727, "lon": -73.9837, "name": "Lincoln Square"},
    22: {"lat": 40.7581, "lon": -73.9171, "name": "Saffron Indian Cuisine"},
    23: {"lat": 40.7101, "lon": -74.0108, "name": "Financial District"},
    24: {"lat": 40.6531, "lon": -73.9698, "name": "Prospect Park Lake"},
    25: {"lat": 40.761, "lon": -73.9682, "name": "Sutton (Midtown East)"},
    26: {"lat": 40.7497, "lon": -73.9913, "name": "Penn Station"},
    27: {"lat": 40.7765, "lon": -73.9549, "name": "Yorkville"},
    28: {"lat": 40.735, "lon": -73.9872, "name": "Gramercy Park"},
    29: {"lat": 40.798835, "lon": -73.9414142, "name": "East Harlem"},
}

REGION_COORDINATES=[
    [40.6911, -73.9351],
    [40.7628, -73.9806],
    [40.721586, -74.001703],
    [40.645794, -73.784486],
    [40.7838, -73.9521],
    [40.7325, -74.002],
    [40.771788, -73.869354],
    [40.7588, -73.9914],
    [40.8293, -73.941],
    [40.7474, -73.9398],
    [40.7531, -73.976],
    [40.7841, -73.9768],
    [40.687, -73.9852],
    [40.7241, -73.9881],
    [40.7246, -73.847],
    [40.743, -74.0013],
    [40.7688, -73.9596],
    [40.7439, -73.982],
    [40.7951, -73.9689],
    [40.8084, -73.9583],
    [40.7151, -73.9549],
    [40.7727, -73.9837],
    [40.7581, -73.9171],
    [40.7101, -74.0108],
    [40.6531, -73.9698],
    [40.761, -73.9682],
    [40.7497, -73.9913],
    [40.7765, -73.9549],
    [40.735, -73.9872],
    [40.798835, -73.9414142]
]



@router.get("/regions")
async def get_all_regions():
    return REGION_COORDINATES_NAMES
