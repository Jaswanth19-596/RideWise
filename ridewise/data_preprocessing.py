import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path
import os
import joblib
import yaml

with open('params.yaml') as stream:
    try:
        params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Loading variables
chunk_size = params['data_preprocessing']['chunk_size']
n_clusters = params['data_preprocessing']['n_clusters']
epsilon_val = params['data_preprocessing']['epsilon_val']




PROJECT_ROOT = Path(__file__).resolve().parents[1]

data_path = os.path.join(PROJECT_ROOT, 'data', 'interim', 'data.csv')
data_reader = pd.read_csv(data_path, chunksize=chunk_size, usecols = ['pickup_longitude', 'pickup_latitude'])

scaler = StandardScaler()
for data_chunk in data_reader:
    scaler.partial_fit(data_chunk)


kmeans = MiniBatchKMeans(n_clusters=n_clusters)

data_reader = pd.read_csv(data_path, chunksize=chunk_size, usecols = ['pickup_longitude', 'pickup_latitude'])
for data_chunk in data_reader:
    scaled_chunk = scaler.transform(data_chunk)
    kmeans.partial_fit(scaled_chunk)


# Read the data into a dataframe
df = pd.read_csv(data_path)

# Scale the data using the scaler
scaled_data = scaler.transform(df[['pickup_longitude', 'pickup_latitude']])

# Assign regions to each combination of latitude and longitude
df['region'] = kmeans.predict(scaled_data)

# Drop the unnecessary columns.
df = df.drop(columns = ['pickup_longitude', 'pickup_latitude'])

# Convert the datatype of the datetime column
df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])

# Set the datetime column as index
df = df.set_index('tpep_pickup_datetime')

# Resampling the data for every 15 mins
resampled_data = df.groupby('region').resample('15min').count()

# Change the name of the new column.
resampled_data.columns = ['total_pickups']

# Make the region a new column
resampled_data = resampled_data.reset_index(level = 0)

# Fill the missing values
resampled_data = resampled_data.replace({'total_pickups': {0 : epsilon_val}})

# Save the dataframe
SAVE_PATH  = os.path.join(PROJECT_ROOT, 'data', 'processed', 'data.csv')
resampled_data.to_csv(SAVE_PATH)

# Save the scaler and the kmeans model
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models')
os.makedirs(MODEL_PATH, exist_ok=True)

joblib.dump(scaler, os.path.join(MODEL_PATH, 'scaler.joblib'))
joblib.dump(kmeans, os.path.join(MODEL_PATH, 'kmeans.joblib'))




