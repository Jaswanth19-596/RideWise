from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error
import os
from xgboost import XGBRegressor
from pathlib import Path
import mlflow
from mlflow.models import infer_signature
from dotenv import load_dotenv

load_dotenv()

# By default MLflow logs to the Databricks-hosted workspace tracking server. You can connect to a different server using the tracking URI.
mlflow.set_tracking_uri("databricks")

# Set experiment in the tracking server
mlflow.set_experiment("/Users/madhajaswanth@gmail.com/Uber_Demand_Prediction")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
train_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'train.csv')
val_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'val.csv')
test_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'test.csv')


train_featured = pd.read_csv(train_path, index_col = 'tpep_pickup_datetime')
val_featured = pd.read_csv(val_path, index_col = 'tpep_pickup_datetime')
test_featured = pd.read_csv(test_path, index_col = 'tpep_pickup_datetime')


# Define feature columns
feature_cols = list(train_featured.columns)
feature_cols.remove('total_pickups')

# Split into X and y
X_train = train_featured[feature_cols]
y_train = train_featured['total_pickups']

X_val = val_featured[feature_cols]
y_val = val_featured['total_pickups']

X_test = test_featured[feature_cols]
y_test = test_featured['total_pickups']



encoder = ColumnTransformer([
    ("ohe", OneHotEncoder(drop="first", sparse_output=False, handle_unknown='ignore'),
     ["region"])
], remainder="passthrough")

X_train_encoded = encoder.fit_transform(X_train)
X_val_encoded = encoder.transform(X_val)
X_test_encoded = encoder.transform(X_test)


params = {
    "colsample_bylevel": 0.7775133568129348,
    "colsample_bynode": 0.5276028563384744,
    "colsample_bytree": 0.831239701417107,
    "gamma": 0.4568672402027697,
    "grow_policy": "depthwise",
    "learning_rate": 0.09036709667822714,
    "max_bin": 128,
    "max_delta_step": 8.208718790843026,
    "max_depth": 12,
    "min_child_weight": 9,
    "n_estimators": 784,
    "reg_alpha": 6.82389041737408,
    "reg_lambda": 8.066313006261286,
    "scale_pos_weight": 1.9992550377663074,
    "subsample": 0.7365551401220525
}


model = XGBRegressor(**params)

model.fit(X_train_encoded, y_train)

y_train_pred = model.predict(X_train_encoded)
y_val_pred = model.predict(X_val_encoded)
y_test_pred = model.predict(X_test_encoded)

# Mean absolute percentage error
train_mape = mean_absolute_percentage_error(y_train, y_train_pred)
val_mape = mean_absolute_percentage_error(y_val, y_val_pred)
test_mape = mean_absolute_percentage_error(y_test, y_test_pred)

# Mean absolute error
train_mae = mean_absolute_error(y_train, y_train_pred)
val_mae = mean_absolute_error(y_val, y_val_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)

metrics = {
    'Train MAPE': train_mape,
    'Val MAPE': val_mape,
    'Test MAPE': test_mape,
    'Train MAE': train_mae,
    'Val MAE': val_mae,
    'Test MAE': test_mae
}


with mlflow.start_run():
    # Log the parameters
    mlflow.log_params(params)

    # Log the model
    signature = infer_signature(X_train_encoded, y_train_pred)
    mlflow.xgboost.log_model(model, signature = signature)

    # Log the metrics
    mlflow.log_metrics(metrics)




