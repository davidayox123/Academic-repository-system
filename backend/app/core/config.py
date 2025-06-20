from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import Optional, Union

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Academic Repository System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database settings
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/academic_repo_db"
    DATABASE_ECHO: bool = False
    
    # Security settings
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: list = [
        "pdf", "doc", "docx", "txt", "md",
        "jpg", "jpeg", "png", "gif",
        "mp4", "avi", "mov",
        "xlsx", "xls", "csv",
        "pptx", "ppt", "py", "js", "ts", "html", "css", "json"    ]
    
    # Email settings (for notifications)
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
      # CORS settings
    CORS_ORIGINS: Union[str, list[str]] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    @field_validator('CORS_ORIGINS')
    @classmethod
    def validate_cors_origins(cls, v):
        """Validate and parse CORS origins"""
        if isinstance(v, str):
            # Split comma-separated string and clean up
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        elif isinstance(v, list):
            return v
        else:
            return [str(v)]
    
    # Pagination settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
