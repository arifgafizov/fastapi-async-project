from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 8000
    database_url: str = 'postgresql+asyncpg://lms_user:superpassword@db/lms_db'
    jwt_secret: str = 'dsEfAyhEoHW1CRP4-X4dWlBxuAB0ibFNm8WB3yayllw'
    jwt_refresh_secret: str = 'Bsfmjvu9bBqXwXuYYS3k35h1DpIQfcWPra2fXlqdoqg'
    jwt_algorithm: str = 'HS256'
    jwt_access_expiration: int = 3600
    jwt_refresh_expiration: int = 10800


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
# c