import pytest
import mlflow
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error
import joblib
from pandas.testing import assert_index_equal

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_PATH = PROJECT_ROOT / 'models'
DATA_PATH = PROJECT_ROOT / 'data'

load_dotenv()

# By default MLflow logs to the Databricks-hosted workspace tracking server. You can connect to a different server using the tracking URI.
mlflow.set_tracking_uri("databricks")

# Set experiment in the tracking server
mlflow.set_experiment("/Users/madhajaswanth@gmail.com/RideWise")


def load_model():
    model_name = "ridewise.development.xgboost"
    alias = "latest"

    model_uri = f"models:/{model_name}@{alias}"
    model = mlflow.xgboost.load_model(model_uri)
    return model



def test_model_loading():
    model = load_model()
    assert model is not None

def test_performance():
    model = load_model()
    test_data = pd.read_csv(DATA_PATH / 'processed' / 'test.csv', parse_dates = ['tpep_pickup_datetime'], index_col = 'tpep_pickup_datetime')
    encoder = joblib.load(MODELS_PATH / 'encoder.joblib')

    X = test_data.drop(columns = 'total_pickups')
    y_true = test_data['total_pickups']

    X_encoded = encoder.transform(X)

    y_pred = model.predict(X_encoded)

    percentage_error = mean_absolute_percentage_error(y_true, y_pred)
    assert percentage_error < 0.3


def test_data_integrity():
    test_data = pd.read_csv(
        DATA_PATH / 'processed' / 'test.csv',
        parse_dates=['tpep_pickup_datetime'],
        index_col='tpep_pickup_datetime'
    )

    expected_columns = [
        "region",
        "hour",
        "day_of_week",
        "day_of_month",
        "is_weekend",
        "is_rush_hour",
        "lag_1",
        "lag_2",
        "lag_3",
        "lag_4",
        "lag_5",
        "lag_6",
        "lag_7",
        "lag_8",
        "rolling_mean_4",
        "rolling_std_4",
        "rolling_mean_8",
        "rolling_std_8",
        "rolling_mean_12",
        "rolling_std_12",
        "rolling_mean_16",
        "rolling_std_16",
        "region_hour_mean",
        "region_hour_std",
        "region_dow_mean",
        "region_dow_std"
        ]
    
    test_data_columns = test_data.drop(columns = 'total_pickups').columns
    
    assert_index_equal(test_data_columns, pd.Index(expected_columns), 
                       exact=True, check_names=True)


    # Checking for missing columns
    missing_values_count = test_data.isna().sum().sum()

    assert missing_values_count == 0, f'Missing value check failed! Found {missing_values_count} missing values'





def test_ranges():
    test_data = pd.read_csv(DATA_PATH / 'processed' / 'test.csv', parse_dates = ['tpep_pickup_datetime'], index_col = 'tpep_pickup_datetime')

    # Region Range Check
    assert ((test_data['region'] < 0) | (test_data['region'] > 30)).sum() == 0, f'The column region in the test data is out of range'

    # Hour Range Check
    assert ((test_data['hour'] < 0) | (test_data['hour'] > 23)).sum() == 0, f'The column hour in the test data is out of range'

    



