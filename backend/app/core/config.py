import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Crochet Visualizer API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./crochet_app.db")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock")

settings = Settings()
