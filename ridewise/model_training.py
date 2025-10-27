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
test_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'test.csv')


train_featured = pd.read_csv(train_path, index_col = 'tpep_pickup_datetime')
test_featured = pd.read_csv(test_path, index_col = 'tpep_pickup_datetime')


# Define feature columns
feature_cols = list(train_featured.columns)
feature_cols.remove('total_pickups')

# Split into X and y
X_train = train_featured[feature_cols]
y_train = train_featured['total_pickups']


X_test = test_featured[feature_cols]
y_test = test_featured['total_pickups']



encoder = ColumnTransformer([
    ("ohe", OneHotEncoder(drop="first", sparse_output=False, handle_unknown='ignore'),
     ["region"])
], remainder="passthrough")

X_train_encoded = encoder.fit_transform(X_train)
X_test_encoded = encoder.transform(X_test)


xg_boost_params = params['model_training']['xg_boost']

model = XGBRegressor(**params)

model.fit(X_train_encoded, y_train)

y_train_pred = model.predict(X_train_encoded)
y_test_pred = model.predict(X_test_encoded)

# Mean absolute percentage error
train_mape = mean_absolute_percentage_error(y_train, y_train_pred)
test_mape = mean_absolute_percentage_error(y_test, y_test_pred)

# Mean absolute error
train_mae = mean_absolute_error(y_train, y_train_pred)
test_mae = mean_absolute_error(y_test, y_test_pred)

metrics = {
    'Train MAPE': train_mape,
    'Test MAPE': test_mape,
    'Train MAE': train_mae,
    'Test MAE': test_mae
}


with mlflow.start_run() as run:
    # Log the parameters
    mlflow.log_params(params)

    # Log the model
    signature = infer_signature(X_train_encoded, y_train_pred)
    mlflow.xgboost.log_model(model, signature = signature, name = 'model')

    # Log the metrics
    mlflow.log_metrics(metrics)


# Registering the model
model_uri = f'runs:/{run.info.run_id}/model'
model_name = "ridewise.development.xg_boost"
model_version = mlflow.register_model(model_uri, model_name)

# Save the scaler and the kmeans model
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models')
os.makedirs(MODEL_PATH, exist_ok=True)
joblib.dump(model, 'models/model.joblib')
joblib.dump(encoder, 'models/encoder.joblib')
