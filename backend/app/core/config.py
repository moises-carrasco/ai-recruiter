"""
Application configuration settings.
"""

from typing import List
from pathlib import Path
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

ENV_PATH = Path(__file__).resolve().parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "AI Technical Interview System"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = f"sqlite:///{PROJECT_ROOT / 'interview_system.db'}"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:3003", "http://127.0.0.1:3003"]
    
    # AI Service
    AI_API_KEY: str = ""
    AI_API_URL: str = "https://api.openai.com/v1"
    AI_MODEL: str = "gpt-3.5-turbo"
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = f"{ENV_PATH}/.env"


settings = Settings()
