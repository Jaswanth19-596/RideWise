import pandas as pd
import numpy as np
import dask.dataframe as dd
from pathlib import Path
import os
import yaml

with open('params.yaml') as stream:
    try:
        params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(f'Exception while loading params.yml', exc)


# Defining bounding box of newyork
min_latitude = params['data_ingestion']['min_latitude']
max_latitude = params['data_ingestion']['max_latitude']
min_longitude = params['data_ingestion']['min_longitude']
max_longitude = params['data_ingestion']['max_longitude']

# Defining max and min fare amount
max_fare_amount = params['data_ingestion']['max_fare_amount']
min_fare_amount = params['data_ingestion']['min_fare_amount']

# Defining max and min trip distance
max_trip_distance = params['data_ingestion']['max_trip_distance']
min_trip_distance = params['data_ingestion']['min_trip_distance']


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

# Removing the outliers
df = df.loc[df['pickup_latitude'].between(min_latitude, max_latitude) & df['pickup_longitude'].between(min_longitude, max_longitude) &
             df['dropoff_latitude'].between(min_latitude, max_latitude) & df['dropoff_longitude'].between(min_longitude, max_longitude) &
             df['fare_amount'].between(min_fare_amount, max_fare_amount) & df['trip_distance'].between(min_trip_distance, max_trip_distance)
            ]

df = df.drop(columns = ['dropoff_latitude', 'dropoff_longitude', 'fare_amount', 'trip_distance'])


df = df.compute()


SAVE_PATH = os.path.join(PROJECT_ROOT, 'data', 'interim')
df.to_csv(os.path.join(SAVE_PATH, 'data.csv'), index = False)


