import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.utils.config import settings
from backend.utils.auth import create_access_token, get_password_hash, verify_password
from backend.models.database import get_db
from backend.models.schemas import User, UserCreate, UserLogin

router = APIRouter(prefix="/api/auth", tags=["auth"])
logger = logging.getLogger(__name__)

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

@router.post("/register", response_model=AuthResponse)
async def register(user_in: UserCreate):
    db = get_db()
    
    # Check if user exists
    if db.users.find_one({"email": user_in.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
        
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_in.password)
    
    new_user = {
        "id": user_id,
        "email": user_in.email,
        "name": user_in.name,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    db.users.insert_one(new_user)
    
    access_token = create_access_token(data={"sub": user_id})
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=User(
            id=user_id,
            email=user_in.email,
            name=user_in.name
        )
    )

@router.post("/login", response_model=AuthResponse)
async def login(user_in: UserLogin):
    db = get_db()
    
    user = db.users.find_one({"email": user_in.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user["id"]})
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=User(
            id=user["id"],
            email=user["email"],
            name=user.get("name")
        )
    )
