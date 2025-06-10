from fastapi import HTTPException, status
from typing import Any, Dict, Optional

__all__ = [
    "AppError",
    "ApiError",
    "ConfigError",
    "ExternalServiceError",
    "LLMError",
    "TelegramError",
    "WeatherApiError",
    "MapsApiError",
    "TranslationApiError",
]


class AppError(Exception):
    """Base error class for application exceptions."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ConfigError(AppError):
    """Error raised when configuration issues occur."""

    pass


class ApiError(HTTPException):
    """Base class for API errors, extends FastAPI's HTTPException."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: Any = "An unexpected error occurred",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class ExternalServiceError(AppError):
    """Base class for errors related to external service integration."""

    def __init__(self, service_name: str, message: str):
        self.service_name = service_name
        super().__init__(f"{service_name} service error: {message}")


class LLMError(ExternalServiceError):
    """Error raised when LLM service fails."""

    def __init__(self, message: str):
        super().__init__("LLM", message)


class TelegramError(ExternalServiceError):
    """Error raised when Telegram API interactions fail."""

    def __init__(self, message: str):
        super().__init__("Telegram", message)


class WeatherApiError(ExternalServiceError):
    """Error raised when Weather API calls fail."""

    def __init__(self, message: str):
        super().__init__("Weather", message)


class MapsApiError(ExternalServiceError):
    """Error raised when Maps API calls fail."""

    def __init__(self, message: str):
        super().__init__("Maps", message)


class TranslationApiError(ExternalServiceError):
    """Error raised when Translation API calls fail."""

    def __init__(self, message: str):
        super().__init__("Translation", message)
