from fastapi import APIRouter, FastAPI

from app.api.routers import health, telegram, admin

__all__ = ["include_routers"]


def include_routers(app: FastAPI) -> None:
    """
    Include all API routers in the FastAPI application.
    
    Args:
        app: The FastAPI application instance
    """
    # Create API router with prefix
    api_router = APIRouter(prefix="/api/v1")
    
    # Include all sub-routers
    api_router.include_router(health.router, tags=["health"])
    api_router.include_router(telegram.router, tags=["telegram"])
    api_router.include_router(admin.router, tags=["admin"])
    
    # Include the API router in the app
    app.include_router(api_router)
