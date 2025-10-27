from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_percentage_error, mean_absolute_error
import os
from xgboost import XGBRegressor
from pathlib import Path
import mlflow
from mlflow.models import infer_signature
from dotenv import load_dotenv
import joblib
import yaml

with open('params.yaml') as stream:
    try:
        params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

load_dotenv()

# By default MLflow logs to the Databricks-hosted workspace tracking server. You can connect to a different server using the tracking URI.
mlflow.set_tracking_uri("databricks")

# Set experiment in the tracking server
mlflow.set_experiment("/Users/madhajaswanth@gmail.com/RideWise")

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


xg_boost_params = params['model_training']['xgboost']

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

# Save the scaler and the kmeans model
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models')
os.makedirs(MODEL_PATH, exist_ok=True)
joblib.dump(model, 'models/model.joblib')
