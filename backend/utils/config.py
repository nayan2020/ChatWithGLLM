from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    google_api_key: str
    faiss_db_path: str = os.path.join(os.getcwd(), "backend", "faiss_db")

    class Config:
        env_file = ".env"

settings = Settings()