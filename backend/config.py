"""
Configuration management using Pydantic Settings.
Loads and validates environment variables required for the backend.

Supports both local development (.env file) and Vercel deployment (env vars).
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Backend directory (where this file lives)
BACKEND_DIR = Path(__file__).parent

# Check if running on Vercel (Vercel sets this automatically)
IS_VERCEL = os.environ.get("VERCEL", "0") == "1"

# Look for .env in multiple locations:
# 1. Backend directory itself (for standalone deployment)
# 2. Parent directory (for monorepo setup with root .env)
def find_env_file() -> Optional[Path]:
    if IS_VERCEL:
        return None

    # Check backend/.env first
    backend_env = BACKEND_DIR / ".env"
    if backend_env.exists():
        return backend_env

    # Then check parent (project root)/.env
    root_env = BACKEND_DIR.parent / ".env"
    if root_env.exists():
        return root_env

    return None

env_file_path = find_env_file()


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
        env_file=str(env_file_path) if env_file_path else None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
# This will fail fast on import if required environment variables are missing
settings = Settings()
