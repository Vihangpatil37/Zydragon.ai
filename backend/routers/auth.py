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

TIER_CONFIG = {
    # Group 1 - Gold (Free + Gold Access)
    "jyash1730@gmail.com": {"tier": "gold", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free"]},
    "manjit19102004@gmail.com": {"tier": "gold", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free"]},
    "jagrut@ao.com": {"tier": "gold", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free"]},
    "vikas@ao.com": {"tier": "gold", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free"]},
    "aditya@ao.com": {"tier": "gold", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free"]},
    
    # Group 2 - Premium (Free + Gold + Premium Access)
    "ananyatarungarg@gmail.com": {"tier": "premium", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free", "zydrakon-premium"]},
    "vijay@ao.com": {"tier": "premium", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free", "zydrakon-premium"]},
    "pranav@ao.com": {"tier": "premium", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free", "zydrakon-premium"]},
    "rajagamer8@gmail.com": {"tier": "premium", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free", "zydrakon-premium"]},
    "vihangpatil37@gmail.com": {"tier": "premium", "allowed_models": ["zydrakon-free", "zhipu-free", "meta-llama/llama-3-8b-instruct:free", "zydrakon-premium"]},
}


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

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
        
    # Sync with TIER_CONFIG to upgrade/downgrade dynamically on login
    tier_info = TIER_CONFIG.get(user["email"].lower().strip())
    if tier_info:
        if user.get("tier") != tier_info["tier"] or user.get("allowed_models") != tier_info["allowed_models"]:
            db.users.update_one(
                {"id": user["id"]}, 
                {"$set": {"tier": tier_info["tier"], "allowed_models": tier_info["allowed_models"]}}
            )
            user["tier"] = tier_info["tier"]
            user["allowed_models"] = tier_info["allowed_models"]
            
    access_token = create_access_token(data={"sub": user["id"]})
    
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=User(
            id=user["id"],
            email=user["email"],
            name=user.get("name"),
            tier=user.get("tier", "free"),
            allowed_models=user.get("allowed_models")
        )
    )
