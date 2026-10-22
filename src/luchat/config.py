import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str


def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
         raise RuntimeError("OPENAI_API_KEY is missing")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    return Settings(openai_api_key=api_key, openai_model=model)