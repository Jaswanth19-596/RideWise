import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from datetime import timedelta
from config import settings
import mlflow
from mlflow.tracking import MlflowClient
import logging

logger = logging.getLogger(__name__)

class TaxiDemandPredictor:
    def __init__(self):
        self.model = None
        self.train_stats = None
        self.test_data = None
        self.encoder = None
        self.initialized = False
        
        try:
            self._initialize()
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {e}")
            logger.warning("Predictor will run in degraded mode")
    
    def _initialize(self):
        """Initialize the predictor with model and data"""
        mlflow.set_tracking_uri("databricks")

        # Creating the model URI
        model_uri = f'models:/{settings.MODEL_NAME}@{settings.MODEL_ALIAS}'

        # Loading the model
        self.model = mlflow.xgboost.load_model(model_uri)

        client = MlflowClient()
        model_version = client.get_model_version_by_alias(
            name=settings.MODEL_NAME,
            alias=settings.MODEL_ALIAS
        )

        run_id = model_version.run_id
        local_path = client.download_artifacts(run_id, '', '.')

        print(f"Artifacts downloaded in {local_path}")

        self.train_stats = settings.TRAIN_STATS_PATH
        self.test_data = pd.read_csv(
            settings.TEST_DATA_PATH,
            parse_dates=['tpep_pickup_datetime'],
            index_col='tpep_pickup_datetime'
        )
        self.encoder = joblib.load(settings.ENCODER_PATH)

        self.initialized = True
        print("✅ Predictor initialized successfully")
    
    def get_simulation_time(self) -> pd.Timestamp:
        """Map current time to March 2024"""
        now = datetime.now()
        return pd.Timestamp(
            year=2016,
            month=3,
            day=min(now.day, 31),
            hour=now.hour,
            minute=now.minute
        )
    
    def compute_features(self, region_id: int, current_time: pd.Timestamp) -> pd.DataFrame:
        """Compute all features for prediction"""
        if not self.initialized:
            raise RuntimeError("Predictor not initialized - model loading failed")
        
        overlim = current_time.minute % 15
        # Move time forward to the start of the next 15-minute bin
        current_time = current_time + timedelta(minutes=15 - overlim)
        
        # Use string indexing to select the time slice
        result_data = self.test_data.loc[str(current_time)] 

        # Ensure result_data is a DataFrame if only one row was returned
        if isinstance(result_data, pd.Series):
            result_data = result_data.to_frame().T 

        mask = (result_data['region'] == region_id)
        result_data = result_data[mask]
        
        return result_data
    
    def predict(self, region_id: int) -> dict:
        """Generates the prediction and returns it as a dictionary with features."""
        if not self.initialized:
            # Return mock data when model isn't loaded
            logger.warning(f"Returning mock prediction for region {region_id}")
            return {
                "prediction": float(np.random.uniform(5, 20)),
                "features": {
                    "is_rush_hour": False,
                    "is_weekend": False,
                },
                "status": "mock_data"
            }
        
        result_data = self.compute_features(region_id, self.get_simulation_time())
        
        if result_data.empty:
            raise ValueError(f"No historical data found for region {region_id} at simulated time.")

        # Extract features before transforming the data
        features = {
            'is_rush_hour': bool(result_data['is_rush_hour'].iloc[0]) if 'is_rush_hour' in result_data.columns else False,
            'is_weekend': bool(result_data['is_weekend'].iloc[0]) if 'is_weekend' in result_data.columns else False,
        }
        transformed_data = self.encoder.transform(result_data)

        prediction = self.model.predict(transformed_data)
        
        return {
            "prediction": float(prediction[0]),
            "features": features,
            "status": "success"
        } 

# Global instance
predictor = TaxiDemandPredictor()