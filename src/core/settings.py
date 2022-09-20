from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '0.0.0.0'
    server_port: int = 8000
    database_url: str = 'postgresql+asyncpg://lms_user:superpassword@db/lms_db'
    jwt_secret: str = '8IJpynryNr5QDcXILDFhd7usM4UPAAvPauTXvUV9aW0'
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
