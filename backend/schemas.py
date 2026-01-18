"""
Pydantic schemas for request/response validation.
Defines data transfer objects for API endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class TaskResponse(BaseModel):
    """
    Task response schema.
    Used for GET, POST, PUT, PATCH responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    user_id: str


class TaskCreate(BaseModel):
    """
    Task creation schema.
    Used for POST /api/{user_id}/tasks
    """
    title: str = Field(
        min_length=1,
        max_length=500,
        description="Task title (required, 1-500 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Task description (optional, max 5000 characters)"
    )


class TaskUpdate(BaseModel):
    """
    Task full update schema.
    Used for PUT /api/{user_id}/tasks/{task_id}
    All fields are required for PUT (full replacement).
    """
    title: str = Field(
        min_length=1,
        max_length=500,
        description="Task title (required)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Task description (optional)"
    )

    completed: bool = Field(
        description="Task completion status (required)"
    )


class TaskPatch(BaseModel):
    """
    Task partial update schema.
    Used for PATCH /api/{user_id}/tasks/{task_id}
    All fields are optional for PATCH (partial update).
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Task title (optional)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Task description (optional)"
    )

    completed: Optional[bool] = Field(
        default=None,
        description="Task completion status (optional)"
    )


# Authentication Schemas

class UserRegister(BaseModel):
    """
    User registration schema.
    Used for POST /auth/register
    """
    email: EmailStr = Field(
        description="User email address"
    )

    password: str = Field(
        min_length=8,
        max_length=100,
        description="User password (min 8 characters)"
    )

    name: str = Field(
        min_length=1,
        max_length=255,
        description="User display name"
    )


class UserLogin(BaseModel):
    """
    User login schema.
    Used for POST /auth/login
    """
    email: EmailStr = Field(
        description="User email address"
    )

    password: str = Field(
        description="User password"
    )


class UserResponse(BaseModel):
    """
    User response schema (without password).
    Used in authentication responses.
    """
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    name: str
    created_at: datetime


class AuthResponse(BaseModel):
    """
    Authentication response schema.
    Returned on successful login/register.
    """
    user: UserResponse
    token: str = Field(
        description="JWT authentication token"
    )
