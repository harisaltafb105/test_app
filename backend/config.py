"""
Configuration management using Pydantic Settings.
Loads and validates environment variables required for the backend.

Supports both local development (.env file) and Vercel deployment (env vars).
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Find project root (parent of backend directory)
PROJECT_ROOT = Path(__file__).parent.parent

# Check if running on Vercel (Vercel sets this automatically)
IS_VERCEL = os.environ.get("VERCEL", "0") == "1"

# Only use .env file if it exists and we're not on Vercel
env_file_path = PROJECT_ROOT / ".env"
USE_ENV_FILE = env_file_path.exists() and not IS_VERCEL


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings are required and must be provided via environment variables
    or a .env file in the project root.

    On Vercel, environment variables are set directly in the dashboard.
    Locally, they are loaded from .env file.
    """

    # Better Auth Configuration
    better_auth_url: str
    better_auth_secret: str

    # Database Configuration
    database_url: str

    # Optional: Frontend URL for CORS (set in Vercel dashboard for production)
    frontend_url: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=str(env_file_path) if USE_ENV_FILE else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
# This will fail fast on import if required environment variables are missing
settings = Settings()
