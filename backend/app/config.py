import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
    DATABASE_URL: str = "sqlite:///./data/ba-ai.db"

settings = Settings()
