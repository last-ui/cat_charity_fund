from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Фонд поддержки котиков'
    description: str = 'Сбор пожертвований на целевые проекты'
    database_url: str = 'sqlite+aiosqlite:///default.db'
    secret: str = 'SECRET_WORD'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    jwt_lifetime: int = 60 * 60 * 24

    class Config:
        env_file = '.env'


settings = Settings()
