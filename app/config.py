import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    embedding_model: str = os.environ.get("EMBEDDING_MODEL", "text-embedding-ada-002")
    llm_model: str = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
    top_n: int = int(os.environ.get("TOP_N", 5))
    use_verifier: bool = os.environ.get("USE_VERIFIER", "1") == "1"


settings = Settings()
