from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
from typing import Callable, Dict, Any
import json

from app.utils.logger import get_app_logger
from app.core.errors import AppError, ApiError

__all__ = ["ErrorHandlingMiddleware", "configure_middleware"]

logger = get_app_logger(module_name="core.middleware")


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for consistent error handling."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except ApiError as e:
            # ApiError is already properly formatted, just log it
            logger.error(f"API error: {e.detail}")
            return self._json_response(
                status_code=e.status_code, content={"error": e.detail}
            )
        except AppError as e:
            # Convert application errors to proper API responses
            logger.error(f"Application error: {e.message}")
            return self._json_response(status_code=500, content={"error": e.message})
        except Exception as e:
            # Catch-all for unexpected errors
            logger.error(f"Unexpected error: {str(e)}")
            logger.debug(traceback.format_exc())

            # In production, we'd hide the actual error details
            return self._json_response(
                status_code=500, content={"error": "An unexpected error occurred"}
            )

    def _json_response(self, status_code: int, content: Dict[str, Any]) -> Response:
        return Response(
            content=json.dumps(content),
            status_code=status_code,
            media_type="application/json",
        )


def configure_middleware(app: FastAPI) -> None:
    """
    Configure all middleware for the application.

    Args:
        app: The FastAPI application instance
    """
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Custom error handling middleware
    app.add_middleware(ErrorHandlingMiddleware)
