from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    APP: str = 'app'
    SECRET_KEY: str = 'secret'

    DEBUG: bool = True

    REDIS_HOST: Optional[str] = 'localhost'
    REDIS_PORT: Optional[str] = 6379
    REDIS_PASSWORD: Optional[str] = None

    REDIS_BACKEND_HEALTH_CHECK_INTERVAL: Optional[int] = 10
    REDIS_SOCKET_CONNECTION_TIMEOUT: Optional[int] = 1
    REDIS_SOCKET_TIMEOUT: bool = 1
    REDIS_RETRY_ON_TIMEOUT: bool = False
    REDIS_SOCKET_KEEPALIVE: bool = True

    MAX_VALUE_SIZE = 10 * 1024 * 1024  # 10 Mb


settings = Settings()
