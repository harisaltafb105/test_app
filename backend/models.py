"""
SQLModel database models.
Defines the User and Task models and database schema.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column, String
from sqlalchemy import Index


class User(SQLModel, table=True):
    """
    User model for authentication.
    Stores user credentials and profile information.
    """

    __tablename__ = "users"

    # Primary key - auto-generated UUID
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )

    # User credentials
    email: str = Field(
        max_length=255,
        nullable=False,
        unique=True,
        index=True,
        description="User email (unique, used for login)"
    )

    password_hash: str = Field(
        max_length=255,
        nullable=False,
        description="Hashed password (bcrypt)"
    )

    # User profile
    name: str = Field(
        max_length=255,
        nullable=False,
        description="User display name"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user was created"
    )

    # Define indexes
    __table_args__ = (
        Index("idx_email", "email", unique=True),
    )


class Task(SQLModel, table=True):
    """
    Task model representing a user's todo item.

    All tasks are scoped to a user via user_id foreign key.
    This enforces strict user isolation at the database level.
    """

    __tablename__ = "tasks"

    # Primary key - auto-generated UUID
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )

    # Task fields
    title: str = Field(
        max_length=500,
        nullable=False,
        description="Task title (required, 1-500 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        sa_column=Column(String(5000), nullable=True),
        description="Task description (optional, max 5000 characters)"
    )

    completed: bool = Field(
        default=False,
        nullable=False,
        description="Task completion status"
    )

    # Timestamps - auto-managed
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when task was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when task was last updated"
    )

    # Foreign key to user (managed by Better Auth, not in our database)
    user_id: str = Field(
        nullable=False,
        index=True,
        description="User ID from Better Auth JWT token"
    )

    # Define indexes for performance
    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_user_created", "user_id", "created_at"),
    )

    def update_timestamp(self):
        """
        Update the updated_at timestamp to current time.
        Call this before saving after modifications.
        """
        self.updated_at = datetime.utcnow()
