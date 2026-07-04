from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Groq LLM
    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"

    # NewsAPI
    newsapi_key: str = ""

    # Database
    database_url: str = "sqlite:///./energem.db"

    # API Config
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_env: str = "development"

    # LLM Config
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.7

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
