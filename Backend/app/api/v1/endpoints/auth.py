from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_session
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse, Token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_session)
) -> Any:
    """
    Register a new user. The first user to register will automatically be an admin.
    """
    # Check if user with email exists
    statement = select(User).where(User.email == user_in.email)
    result = await db.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
        
    # Check if user with username exists
    statement = select(User).where(User.username == user_in.username)
    result = await db.execute(statement)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="The username is already taken.",
        )
        
    # Check if this is the first user
    statement = select(User)
    result = await db.execute(statement)
    first_user = result.first()
    
    # First user gets admin, otherwise normal user
    role = "admin" if first_user is None else "user"

    user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=get_password_hash(user_in.password),
        role=role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    Using email as the username field in the form.
    """
    # Form data "username" is actually the email in our implementation
    statement = select(User).where(User.email == form_data.username)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user profile.
    """
    return current_user
