from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    MODELS_DIR: Path = Path("models")
    DATA_DIR: Path =  Path("data")
    MODEL_NAME: str = 'ridewise.production.xgboost'
    MODEL_ALIAS: str = 'champion'

    DATABRICKS_HOST:str
    DATABRICKS_TOKEN:str


    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Model files
    KMEANS_PATH: Path = MODELS_DIR / "kmeans.joblib"
    ENCODER_PATH: Path = MODELS_DIR / "encoder.joblib"
    SCALER_PATH: Path = MODELS_DIR / "scaler.joblib"
    TRAIN_STATS_PATH: Path = DATA_DIR /"train_stats.csv"
    TEST_DATA_PATH: Path = DATA_DIR / "test.csv"
    
    class Config:
        env_file = ".env"

settings = Settings()