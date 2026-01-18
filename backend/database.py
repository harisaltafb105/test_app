"""
Database connection and session management using SQLModel with async PostgreSQL.
Configures async engine, session factory, and dependency injection for FastAPI.

Supports both local development (connection pooling) and Vercel serverless (NullPool).
"""

import os
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from backend.config import settings

# Check if running on Vercel serverless
IS_VERCEL = os.environ.get("VERCEL", "0") == "1"

# Create async engine with appropriate pooling strategy
# For serverless (Vercel): Use NullPool to avoid connection pooling issues
# For local: Use connection pooling for better performance
if IS_VERCEL:
    # Serverless: No connection pooling, each request gets a fresh connection
    # This works better with Neon's serverless driver and connection pooler
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        poolclass=NullPool,
    )
else:
    # Local development: Use connection pooling for better performance
    # pool_size: number of permanent connections to maintain
    # max_overflow: additional connections when pool is full
    # pool_pre_ping: verify connection is alive before using it
    engine = create_async_engine(
        settings.database_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )


# Create async session factory
# expire_on_commit=False prevents lazy loading errors after commit
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database session injection.

    Yields an async session and ensures it's closed after use.
    Use this in route dependencies: session: AsyncSession = Depends(get_session)
    """
    async with async_session_factory() as session:
        yield session


async def create_db_and_tables():
    """
    Create all database tables from SQLModel metadata.

    This should be called on application startup.
    In production, use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
