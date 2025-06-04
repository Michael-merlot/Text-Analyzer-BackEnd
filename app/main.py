from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import documents, analysis, readabilityAPI
from app.database.database import Base, engine
from app.core.config import settings
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        print("База данных инициализирована")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    
    yield
    
    print("Приложение завершает работу")

app = FastAPI(
    title=settings.APP_NAME,
    description="API для анализа текстовых документов",
    version="1.0.0",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

os.makedirs("temp", exist_ok=True)

app.include_router(documents.router, prefix=f"{settings.API_PREFIX}/documents", tags=["documents"])
app.include_router(analysis.router, prefix=f"{settings.API_PREFIX}/analysis", tags=["analysis"])
app.include_router(readabilityAPI.router, prefix=f"{settings.API_PREFIX}/readability", tags=["readability"])

@app.get("/", tags=["root"])
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Добро пожаловать в API Текстового Оценщика",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Проверка работоспособности API"""
    return {"status": "healthy"}
