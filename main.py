from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.endpoints import documents, analysis, readability
from app.core.config import settings

'''
���������� ��� ��������� ���, ������� ������� ������� ��� ������� � ���� ������
'''

# �������� ���������� FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API ��� ������� ��������� ����������",
    version="1.0.0",
    lifespan=lifespan
)

# ��������� CORS (����. ��������, ������� ���������� HTTP-��������� � ��������� ���-��������� �������� ������ � ��������)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

# ���������� ��������� API
app.include_router(documents.router, prefix=f"{settings.API_PREFIX}/documents", tags=["documents"])
app.include_router(analysis.router, prefix=f"{settings.API_PREFIX}/analysis", tags=["analysis"])
app.include_router(readability.router, prefix=f"{settings.API_PREFIX}/readability", tags=["readability"])

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "����� ���������� � API ���������� ��������",
        "version": "1.0.0",
        "docs_url": "/docs"
    }
