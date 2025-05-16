import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Japan Honeymoon Travel Assistant"
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    
    # LLM Service
    USE_LOCAL_LLM: bool = Field(True, env="USE_LOCAL_LLM")
    OLLAMA_BASE_URL: str = Field("http://localhost:11434", env="OLLAMA_BASE_URL")
    OLLAMA_MODEL: str = Field("llama3", env="OLLAMA_MODEL")
    
    # Cloud LLM (for fallback)
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: Optional[str] = Field(None, env="GOOGLE_MAPS_API_KEY")
    
    # Weather
    OPENWEATHER_API_KEY: Optional[str] = Field(None, env="OPENWEATHER_API_KEY")
    
    # Translation
    DEEPL_API_KEY: Optional[str] = Field(None, env="DEEPL_API_KEY")
    
    # Configure .env file path
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    def get_llm_credentials(self) -> Dict[str, Any]:
        """Return credentials for the appropriate LLM service."""
        if self.USE_LOCAL_LLM:
            return {
                "base_url": self.OLLAMA_BASE_URL,
                "model": self.OLLAMA_MODEL
            }
        elif self.OPENAI_API_KEY:
            return {"api_key": self.OPENAI_API_KEY}
        elif self.ANTHROPIC_API_KEY:
            return {"api_key": self.ANTHROPIC_API_KEY}
        else:
            raise ValueError("No LLM credentials available")


# Initialize settings instance
settings = Settings() 