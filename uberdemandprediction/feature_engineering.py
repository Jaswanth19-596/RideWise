import pandas as pd
from pathlib import Path
import os

import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).resolve().parents[1]
data_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'data.csv')

df = pd.read_csv(data_path, parse_dates = ['tpep_pickup_datetime'])
df = df.set_index('tpep_pickup_datetime')

# Splitting the data into train, test, val splits
date_series = pd.to_datetime(pd.Series(df.index))

train_end_date = date_series.quantile(0.8)
val_end_date = date_series.quantile(0.9)

train_df = df.loc[df.index <= train_end_date].copy()
val_df = df[(df.index > train_end_date) & (df.index <= val_end_date)].copy()
test_df = df[df.index > val_end_date].copy()

print(f"Train: {train_df.index.min()} to {train_df.index.max()} ({len(train_df)} rows)")
print(f"Val:   {val_df.index.min()} to {val_df.index.max()} ({len(val_df)} rows)")
print(f"Test:  {test_df.index.min()} to {test_df.index.max()} ({len(test_df)} rows)")


def create_time_series_features(df, is_train = False, train_stats = None):

  result = df.copy()

  # A. TIME-BASED FEATURES
  print("Creating Time based features ..")
  result['hour'] = result.index.hour
  result['day_of_week'] = result.index.dayofweek
  result['day_of_month'] = result.index.day
  result['is_weekend'] = (result['day_of_week'] >= 5).astype(int)
  result['is_rush_hour'] = ((result['hour'] >= 7) & (result['hour'] <= 9) | ((result['hour'] >= 17) & (result['hour'] <= 21))).astype(int)

  # B. LAG FEATURES
  print("Creating LAG Features")

  for region in result['region'].unique():
    mask = result['region'] == region

    region_data = result.loc[mask, 'total_pickups']

    for lag in [1, 2, 3, 4, 5, 6, 7, 8]:
      result.loc[mask, f'lag_{lag}'] = region_data.shift(lag)


  # -------------------------
  # C. ROLLING STATISTICS (Trends)
  # -------------------------
  print("  Creating rolling statistics...")

  for region in result['region'].unique():

    mask = result['region'] == region
    region_data = result.loc[mask, 'total_pickups']

    for window in [4, 8, 12, 16]:
      result.loc[mask, f'rolling_mean_{window}'] = region_data.shift(1).rolling(window = window).mean()
      result.loc[mask, f'rolling_std_{window}'] = region_data.shift(1).rolling(window = window).std()


  # D. HISTORICAL STATISTICS
  print("Historical Statistics")

  if is_train:

    # For every region,
    # For every hour,
    # what are the average pickups for that region at that particular hour.
    #
    train_stats = result.groupby(['region', 'hour'])['total_pickups'].agg([
        ('region_hour_mean', 'mean'), ('region_hour_std', 'std')
        ]).reset_index()


    dow_stats = result.groupby(['region', 'day_of_week'])['total_pickups'].agg([
        ('region_dow_mean', 'mean'), ('region_dow_std', 'std')
    ]).reset_index()

    train_stats = train_stats.merge(dow_stats, on = ['region'], how = 'left')


  result = result.reset_index().merge(train_stats, on = ['region', 'hour', 'day_of_week'], how = 'left')
  result = result.set_index('tpep_pickup_datetime')

  result['region_hour_std'] = result['region_hour_std'].fillna(0)
  result['region_dow_std'] = result['region_dow_std'].fillna(0)

  return result, train_stats


train_featured, train_stats = create_time_series_features(train_df, is_train = True)

val_featured, _ = create_time_series_features(val_df, train_stats = train_stats)

test_featured, _ = create_time_series_features(test_df, train_stats = train_stats)

# Drop rows with NaN (from lag features at the beginning)
initial_train_size = len(train_featured)
train_featured = train_featured.dropna()
val_featured = val_featured.dropna()
test_featured = test_featured.dropna()

print(f"\n✓ Dropped {initial_train_size - len(train_featured)} rows with NaN (from lag features)")
print(f"✓ Final shapes: Train={train_featured.shape}, Val={val_featured.shape}, Test={test_featured.shape}")


SAVE_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed')
train_featured.to_csv(os.path.join(SAVE_PATH, 'train.csv'))
val_featured.to_csv(os.path.join(SAVE_PATH, 'val.csv'))
test_featured.to_csv(os.path.join(SAVE_PATH, 'test.csv'))




