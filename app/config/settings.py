from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Union


class Settings(BaseSettings):

    # App info
    PROJECT_NAME: str = "Quiz App"
    VERSION: str = "0.1.1"

    # Huggingface API
    HF_KEY:str = Field(..., env="HF_KEY")

    # LLM Configuration
    GPT_MODEL:str = Field(default='gpt-3.5-turbo-1106', env="GPT_MODEL")
    OPENAI_API_KEY:str = Field(..., env="OPENAI_API_KEY")

    # MongoDB
    MONGO_DATABASE_NAME:str = Field(..., env="MONGO_DATABASE_NAME")
    MONGO_DATABASE_HOST:str = Field(..., env="MONGO_DATABASE_HOST")

    # CORS Settings
    allowed_origins: Union[str, List[str]] = Field(
        default=["*"],
        env="ALLOWED_ORIGINS",
        description="Allowed CORS origins as string or list"
    )
    allowed_methods: Union[str, List[str]] = Field(
        default=["*"],
        env="ALLOWED_METHODS",
        description="Allowed HTTP methods as string or list"
    )
    allowed_headers: Union[str, List[str]] = Field(
        default=["*"],
        env="ALLOWED_HEADERS",
        description="Allowed headers as string or list"
    )

    # Log directory
    LOGS_DIR: str = "app/logs"


    @field_validator("allowed_origins", "allowed_methods", "allowed_headers")
    @classmethod
    def parse_cors_settings(cls, v) -> List[str]:
        if isinstance(v, str):
            # Handle comma-separated string
            if ',' in v:
                return [x.strip() for x in v.split(',') if x.strip()]
            # Handle single string
            return [v.strip()]
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        return ["*"]  # Default fallback
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()