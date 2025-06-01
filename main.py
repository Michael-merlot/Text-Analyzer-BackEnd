from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import documents, analysis, readabilityAPI
from app.database.database import Base, engine
from app.core.config import settings

'''
Необходимо тут прописать код, который создает создает все таблицы в базе данных
'''

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

app.include_router(documents.router, prefix=f"{settings.API_PREFIX}/documents", tags=["documents"])
app.include_router(analysis.router, prefix=f"{settings.API_PREFIX}/analysis", tags=["analysis"])
app.include_router(readabilityAPI.router, prefix=f"{settings.API_PREFIX}/readability", tags=["readability"])

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Добро пожаловать в API Текстового Оценщика",
        "version": "1.0.0",
        "docs_url": "/docs"
    }
