from fastapi import APIRouter, Request

from app.utils.logger import get_app_logger
from app.utils.middleware_logs import get_request_logger

router = APIRouter(prefix="/health", tags=["health"])
logger = get_app_logger(module_name="api.health")


@router.get("")
async def health_check(request: Request):
    """
    Health check endpoint to verify API status.
    Returns a 200 OK response when the API is running.
    """
    request_logger = get_request_logger(request)
    request_logger.info("Health check requested")
    
    return {
        "status": "ok",
        "message": "Japan Honeymoon Travel Assistant API is operational"
    }
