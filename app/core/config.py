from pydantic import BaseSettings
from typing import List, Union
import os
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "���������-�������"
    API_PREFIX: str = "/api"
    DEBUG: bool = True
    
    ALLOWED_MIME: List[str] = ["text/plain"]
    MAX_FILE_SIZE: int = 1 * 1024 * 1024 
    
    DATABASE_URL: str = "???" # ���� ��� �������� ���, ��� ���� ��� ���� ��
    
    ALLOW_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
