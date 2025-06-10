from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import core application components
from app.core.config import settings
from app.core.middleware import configure_middleware
from app.core.container import get_container
from app.api.routers import include_routers
from app.utils.logger import get_app_logger
from app.utils.middleware_logs import (
    RequestLoggingMiddleware,
    ResponseTimeLoggingMiddleware,
)

# Create application logger
logger = get_app_logger(module_name="main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events for the FastAPI application.
    """
    # Startup logic
    logger.info("Application startup")

    # Initialize dependency injection container
    _ = get_container()
    logger.info("Dependency injection container initialized")

    yield

    # Shutdown logic
    logger.info("Application shutdown")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        The configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="A telegram bot providing comprehensive travel assistance for honeymooners in Japan",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Configure middleware
    configure_middleware(app=app)

    # Add logging middleware
    app.add_middleware(middleware_class=RequestLoggingMiddleware)
    app.add_middleware(middleware_class=ResponseTimeLoggingMiddleware)

    # Include API routers
    include_routers(app=app)

    # Add root endpoint
    @app.get("/")
    async def root():
        """Health check endpoint."""
        logger.info("Root endpoint called")
        return {
            "status": "online",
            "message": f"{settings.PROJECT_NAME} API is running",
        }

    return app


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting application server")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
