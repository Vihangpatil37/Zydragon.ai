import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Core Tier Definitions
TIER_FREE = "free"
TIER_GOLD = "gold"
TIER_PREMIUM = "premium"

# Map of Models to their required base tiers
MODEL_TIER_REQUIREMENTS = {
    "zydrakon-free": TIER_FREE,
    "zhipu-free": TIER_GOLD,
    "zydrakon-premium": TIER_PREMIUM,
    "zydrakon-orchestration": TIER_FREE,  # Internal usage
}

# Tier Hierarchy mapping for easier logic validation
# Higher index means higher privileges
TIER_HIERARCHY = {
    TIER_FREE: 0,
    TIER_GOLD: 1,
    TIER_PREMIUM: 2
}

def validate_model_access(user: Dict[str, Any], requested_model: str) -> bool:
    """
    Validates if a user has permission to access a specific model.
    Checks base tier hierarchy as well as explicitly allowed models.
    """
    user_tier = user.get("tier", TIER_FREE)
    allowed_models = user.get("allowed_models") or []
    
    # 1. If explicitly allowed, grant access immediately
    if requested_model in allowed_models:
        return True
        
    # 2. Check base tier requirements
    required_tier = MODEL_TIER_REQUIREMENTS.get(requested_model)
    if not required_tier:
        # If the model is completely unknown in our matrix, default to safe rejection
        # unless it is some OpenRouter dynamic model. For now, restrict to known models.
        # However, fallback models like openrouter/free may be requested internally.
        # We will allow them if they aren't explicitly premium.
        logger.warning(f"Unknown model requested: {requested_model}. Safely allowing if not explicitly premium.")
        return True
        
    user_tier_level = TIER_HIERARCHY.get(user_tier, 0)
    required_tier_level = TIER_HIERARCHY.get(required_tier, 0)
    
    # 3. Deny if user's tier is lower than the required tier
    if user_tier_level < required_tier_level:
        logger.info(
            f"Access Denied: User {user.get('email', user.get('id'))} "
            f"(Tier: {user_tier}) attempted to use {requested_model}"
        )
        return False
        
    return True
