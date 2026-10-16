import os

class Settings:
    PROJECT_NAME: str = "Cardiac Risk Assessment API"
    VERSION: str = "1.0.0"
    MODEL_PATH: str = os.getenv("MODEL_PATH", os.path.join("models", "cardiac_risk_pipeline.joblib"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()