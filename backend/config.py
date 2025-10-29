from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    DATA_DIR: Path = PROJECT_ROOT / "data"

    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Model files
    MODEL_PATH: Path = MODELS_DIR / "model.joblib"
    TRAIN_STATS_PATH: Path = DATA_DIR / "processed" / "train_stats.csv"
    MARCH_DATA_PATH: Path = DATA_DIR / "processed" / "test.csv"
    ENCODER_PATH: Path = MODELS_DIR / "encoder.joblib"
    
    class Config:
        env_file = ".env"

settings = Settings()