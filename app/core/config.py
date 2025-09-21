import os
from functools import lru_cache
from typing import Literal

from importlib import metadata
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_project_version() -> str:
    """从 pyproject.toml 文件中动态读取项目版本号。"""
    try:
        return metadata.version("fastapi-demo-project")
    except metadata.PackageNotFoundError:
        return "0.1.0-dev"


class DatabaseConfig(BaseSettings):
    """数据库相关配置"""
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    DB: str = "app"

    @computed_field()
    @property
    def DATABASE_URL(self) -> str:
        return  f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

    model_config = SettingsConfigDict(env_prefix="DEMO_DB_")


class Settings(BaseSettings):
    ENVIRONMENT: Literal["dev", "prod"] = "dev"

    DEBUG: bool = False
    APP_NAME: str = "fastapi-demo-project"
    DB:DatabaseConfig = DatabaseConfig()

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_prefix="DEMO_",
        case_sensitive=False,
    )

@lru_cache()
def get_settings() -> Settings:
    print("正在加载配置")
    env = os.getenv("ENVIRONMENT", "dev")
    env_file = f".env.{env}"
    settings = Settings(_env_file=env_file)
    print(f"成功加载 '{env}' 环境配置 for {settings.APP_NAME}")
    return settings

settings = get_settings()
