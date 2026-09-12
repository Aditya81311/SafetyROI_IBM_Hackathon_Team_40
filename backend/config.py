from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # Application
    APP_NAME: str = "Road Safety Management Platform"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./road_safety.db"
    
    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
