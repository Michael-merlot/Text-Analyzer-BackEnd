from pydantic import BaseSettings
from typing import List, Union
import os
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "Текстовый-Оценщик" 
    API_PREFIX: str = "/api"             
    DEBUG: bool = True                  
    
    # настройки загрузки файлов
    ALLOWED_MIME: List[str] = ["text/plain"]  
    MAX_FILE_SIZE: int = 1 * 1024 * 1024      
    
    # настройка подключения к базе данных
    DATABASE_URL: str = "???" 
    
    # настройки CORS 
    ALLOW_ORIGINS: List[str] = ["*"]      
    ALLOW_CREDENTIALS: bool = True        
    ALLOW_METHODS: List[str] = ["*"]      
    ALLOW_HEADERS: List[str] = ["*"]      

    class Config:
        env_file = ".env" 

settings = Settings()
