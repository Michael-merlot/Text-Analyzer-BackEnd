from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    APP_NAME: str = "Текстовый-Оценщик" 
    API_PREFIX: str = "/api"             
    DEBUG: bool = True                  
    
    ALLOWED_MIME: List[str] = ["text/plain"]  
    MAX_FILE_SIZE: int = 1 * 1024 * 1024     
    
    DATABASE_URL: str = "sqlite:///./text_analyzer.db"
    
    ALLOW_ORIGINS: List[str] = ["*"]      
    ALLOW_CREDENTIALS: bool = True        
    ALLOW_METHODS: List[str] = ["*"]      
    ALLOW_HEADERS: List[str] = ["*"]      
    
    model_config = {
        "env_file": ".env"
    }

settings = Settings()
