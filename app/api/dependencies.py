from fastapi import Depends, HTTPException, status, Request, Header
from typing import Annotated

from app.utils.logger import get_app_logger
from app.core.config import settings

logger = get_app_logger(module_name="api.dependencies")


async def verify_token(
    request: Request, authorization: Annotated[str, Header()] = None
) -> bool:
    """
    Dependency for verifying API token in authorization header.
    This is a simple implementation that would be expanded with proper auth.

    Args:
        request: The FastAPI request object
        authorization: The authorization header value

    Returns:
        bool: True if token is valid

    Raises:
        HTTPException: If token is missing or invalid
    """
    client_ip = request.client.host if request.client else "unknown"
    
    if not authorization:
        logger.warning(f"Missing authorization header from {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
        )

    # Simple token validation for demonstration
    # In production, use proper authentication
    expected_token = f"Bearer {settings.API_KEY}"
    if authorization != expected_token:
        logger.warning(f"Invalid authorization token from {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization token",
        )
    
    logger.info(f"Successful authentication from {client_ip}")
    return True


# Create a reusable dependency
require_auth = Depends(verify_token)
