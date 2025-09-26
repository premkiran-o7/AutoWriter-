from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Google Gemini API key (if needed for SDK)
    GOOGLE_API_KEY: str
    # LangChain / LLM settings
    GOOGLE_MODEL: str = "gemini-pro"
    # Max news results
    MAX_NEWS_RESULTS: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
