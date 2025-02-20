from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODEL_PATH: str = "../dataset/diabetes-prediction-model.joblib"
    API_PORT: int = 8000
    API_HOST: str = "0.0.0.0"

    class Config:
        env_file = ".env"

settings = Settings()