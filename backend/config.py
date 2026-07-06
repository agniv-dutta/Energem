from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Groq LLM
    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"

    # Claude API
    claude_api_key: str = ""
    claude_model: str = "claude-3-5-sonnet-latest"

    # NewsAPI
    newsapi_key: str = ""
    news_fetch_interval_minutes: int = 60
    news_keywords: list[str] = ["Hormuz", "Houthis", "sanctions", "crude", "OPEC", "Brent"]

    # Database
    database_url: str = "sqlite:///./energem.db"

    # Risk scoring
    corridor_weights: dict[str, float] = {
        "hormuz": 1.5,
        "red_sea": 1.2,
        "malacca": 0.8,
        "suez": 1.0,
        "land_route": 0.9,
    }

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
