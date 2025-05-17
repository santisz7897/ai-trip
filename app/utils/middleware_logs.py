"""
Middleware components for the FastAPI application.
"""

import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import uuid
from app.utils.logger import get_app_logger
import logging

# Create logger for middleware
logger = get_app_logger(module_name="middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.

    This middleware logs:
    1. Request start with method, path, and client IP
    2. Response completion with status code and processing time
    3. Assigns a unique request_id to track requests across logs
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Add request ID to request state for access in route handlers
        request.state.request_id = request_id

        # Log request start
        start_time = time.perf_counter()
        client_host = request.client.host if request.client else "unknown"

        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "client_ip": client_host,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "user_agent": request.headers.get("user-agent", "unknown"),
            },
        )

        # Process the request and get response
        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = time.perf_counter() - start_time

            # Log successful response
            logger.info(
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "processing_time_ms": round(process_time * 1000, 2),
                    "method": request.method,
                    "path": request.url.path,
                },
            )

            # Add request ID to response headers for debugging
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as exc:
            # Calculate processing time
            process_time = time.time() - start_time

            # Log error in request processing
            logger.exception(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    "request_id": request_id,
                    "processing_time_ms": round(process_time * 1000, 2),
                    "method": request.method,
                    "path": request.url.path,
                    "error": str(exc),
                },
            )

            # Re-raise the exception to be handled by FastAPI exception handlers
            raise


class ResponseTimeLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for tracking and logging response times.
    More lightweight than the full RequestLoggingMiddleware.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add processing time header
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))

        return response


def get_request_logger(request: Request) -> logging.Logger:
    """
    Creates a logger with request context data.

    Usage in route functions:
        @app.get("/items")
        async def get_items(request: Request):
            logger = get_request_logger(request)
            logger.info("Getting items")
            # ... function logic ...
    """
    # Create a base logger for the endpoint
    logger = get_app_logger(module_name="api")

    # Extract useful request data
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    client_host = request.client.host if request.client else "unknown"

    # Create context dict to be included with all log entries
    context = {
        "request_id": request_id,
        "client_ip": f"{client_host}:{request.client.port if request.client else 'unknown'}",
        "method": request.method,
        "path": request.url.path,
    }

    # Return a LoggerAdapter that adds context to each log call
    return logging.LoggerAdapter(logger=logger, extra=context)
