from fastapi import APIRouter
from backend.app.api.v1.endpoints import ai, datasets, health

api_v1_router = APIRouter()

# Include sub-routers with tags and prefixes
api_v1_router.include_router(health.router, tags=["Health"])
api_v1_router.include_router(ai.router, prefix="/ai", tags=["AI"])
api_v1_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
