import pandas as pd
import numpy as np
import dask.dataframe as dd
from pathlib import Path
import os

# Defining the project root and Data paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw')

# Use the following columns
use_columns = ['tpep_pickup_datetime', 'pickup_longitude', 'pickup_latitude', 'dropoff_latitude', 'dropoff_longitude', 'trip_distance', 'fare_amount']


# Defining the file paths
jan_path = os.path.join(DATA_PATH, 'yellow_tripdata_2016-01.csv')
feb_path = os.path.join(DATA_PATH, 'yellow_tripdata_2016-02.csv')
mar_path = os.path.join(DATA_PATH, 'yellow_tripdata_2016-03.csv')

# Loading the dataframes
jan_df = dd.read_csv(jan_path, assume_missing = True, usecols = use_columns)
feb_df = dd.read_csv(feb_path, assume_missing = True, usecols = use_columns)
mar_df = dd.read_csv(mar_path, assume_missing = True, usecols = use_columns)

# Concatenating the dataframes into one
df = dd.concat([jan_df, feb_df, mar_df], axis = 0)


# Removing outliers

# Defining bounding box of newyork
min_latitude = 40.60
max_latitude = 40.85
min_longitude = -74.05
max_longitude = -73.70

# Defining max and min fare amount
max_fare_amount = 81
min_fare_amount = 0.5

# Defining max and min trip distance
max_trip_distance = 25
min_trip_distance = 0.25


# Dropping the outliers
df = df.loc[df['pickup_latitude'].between(min_latitude, max_latitude) & df['pickup_longitude'].between(min_longitude, max_longitude) &
             df['dropoff_latitude'].between(min_latitude, max_latitude) & df['dropoff_longitude'].between(min_longitude, max_longitude) &
             df['fare_amount'].between(min_fare_amount, max_fare_amount) & df['trip_distance'].between(min_trip_distance, max_trip_distance)
            ]

df = df.drop(columns = ['dropoff_latitude', 'dropoff_longitude', 'fare_amount', 'trip_distance'])

df = df.compute()


SAVE_PATH = os.path.join(PROJECT_ROOT, 'data', 'interim')
df.to_csv(os.path.join(SAVE_PATH, 'data.csv'), index = False)


