from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str
    DATABASE_URL: str
    USERNAME: str
    PASSWORD: str
    PORT_NUMBER: int
    HOST: str
    
    # 🔒 JWT Authentication settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    IS_REFRESH_TOKEN_AUTOMATIC: bool

    @classmethod
    def from_env(cls):
        return cls(
            # 🌐 App settings
            APP_NAME=os.getenv("APP_NAME", "FastAPI Auth App"),
            DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///./app.db"),
            USERNAME=os.getenv("USERNAME", "postgres"),
            PASSWORD=os.getenv("PASSWORD", "password"),
            PORT_NUMBER=int(os.getenv("PORT_NUMBER", "8000")),
            HOST=os.getenv("HOST", "127.0.0.1"),
            
            # 🔐 Security settings
            SECRET_KEY=os.getenv("SECRET_KEY"),
            ALGORITHM=os.getenv("ALGORITHM"),
            ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
            REFRESH_TOKEN_EXPIRE_MINUTES=int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")),
            IS_REFRESH_TOKEN_AUTOMATIC=os.getenv("IS_REFRESH_TOKEN_AUTOMATIC", "true").lower() == "true"
        )

@lru_cache()
def get_settings():
    return Settings.from_env()
