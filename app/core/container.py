from dependency_injector import containers, providers

from app.utils.logger import get_app_logger
from app.core.config import settings

__all__ = ["Container", "get_container"]

logger = get_app_logger(module_name="core.container")


class Container(containers.DeclarativeContainer):
    """
    Dependency Injection container for the application.

    This container manages the lifecycle of all service instances and their dependencies.
    """

    # Application configuration
    config = providers.Singleton(lambda: settings)

    # External API clients (to be populated in future tasks)
    # Example:
    # llm_client = providers.Factory(
    #     LLMClient,
    #     base_url=config.provided.OLLAMA_BASE_URL,
    #     model=config.provided.OLLAMA_MODEL
    # )

    # Service layer (to be populated in future tasks)
    # Example:
    # llm_service = providers.Singleton(
    #     LLMService,
    #     llm_client=llm_client
    # )


# Singleton container instance
_container = None


def get_container() -> Container:
    """
    Get or create the dependency injection container.

    Returns:
        The singleton container instance
    """
    global _container
    if _container is None:
        logger.info("Initializing dependency injection container")
        _container = Container()

        # Additional container configuration can be done here
        # Example: _container.config.from_dict({"some_value": "test"})

    return _container
