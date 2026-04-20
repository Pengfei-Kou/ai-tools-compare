from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.models import router as models_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(models_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
