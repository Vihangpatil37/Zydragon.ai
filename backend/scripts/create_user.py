import uuid
from datetime import datetime
from backend.models.database import get_db, init_db
from backend.utils.auth import get_password_hash
USERS = [
    {
        "email": "jyash1730@gmail.com",
        "name": "Yash Jain",
        "password": "62661@yash",
        "tier": "gold",
        "allowed_models": ["zydrakon-free", "zhipu-free"]
    },
    {
        "email": "manjit19102004@gmail.com",
        "name": "Manjit",
        "password": "75480@manjit",
        "tier": "gold",
        "allowed_models": ["zydrakon-free", "zhipu-free"]
    },
    {
        "email": "ananyatarungarg@gmail.com",
        "name": "Ananya Garg",
        "password": "75748@ananya",
        "tier": "premium",
        "allowed_models": ["zydrakon-free", "zhipu-free", "zydrakon-premium"]
    },
    {
        "email": "vijay@ao.com",
        "name": "Vijay",
        "password": "98250@vijay",
        "tier": "premium",
        "allowed_models": ["zydrakon-free", "zhipu-free", "zydrakon-premium"]
    },
    {
        "email": "pranav@ao.com",
        "name": "Pranav",
        "password": "98240@pranv",
        "tier": "premium",
        "allowed_models": ["zydrakon-free", "zhipu-free", "zydrakon-premium"]
    },
    {
        "email": "jagrut@ao.com",
        "name": "Jagrut",
        "password": "72030@jagrut",
        "tier": "gold",
        "allowed_models": ["zydrakon-free", "zhipu-free"]
    },
    {
        "email": "vikas@ao.com",
        "name": "Vikas",
        "password": "88664@vikas",
        "tier": "gold",
        "allowed_models": ["zydrakon-free", "zhipu-free"]
    },
    {
        "email": "aditya@ao.com",
        "name": "Aditya",
        "password": "93745@aditya",
        "tier": "gold",
        "allowed_models": ["zydrakon-free", "zhipu-free"]
    },
    {
        "email": "rajagamer8@gmail.com",
        "name": "Raj",
        "password": "87350@raj",
        "tier": "premium",
        "allowed_models": ["zydrakon-free", "zhipu-free", "zydrakon-premium"]
    },
    {
        "email": "vihangpatil37@gmail.com",
        "name": "Vihang",
        "password": "814033@vihang",
        "tier": "premium",
        "allowed_models": ["zydrakon-free", "zhipu-free", "zydrakon-premium"]
    }
]

def create_gold_users():
    init_db()
    db = get_db()
    
    # Clean up typo user if it exists
    deleted = db.users.delete_one({"email": "pranav@a0.com"})
    if deleted.deleted_count > 0:
        print("Removed typo user 'pranav@a0.com' from database.")
    
    for u in USERS:
        email = u["email"]
        name = u["name"]
        password = u["password"]
        tier = u["tier"]
        allowed_models = u["allowed_models"]
        hashed_password = get_password_hash(password)
        
        existing = db.users.find_one({"email": email})
        if existing:
            db.users.update_one(
                {"email": email},
                {"$set": {
                    "name": name,
                    "hashed_password": hashed_password,
                    "tier": tier,
                    "allowed_models": allowed_models
                }}
            )
            print(f"Updated existing user '{email}' ({name}) with {tier.capitalize()} tier.")
        else:
            user_id = str(uuid.uuid4())
            new_user = {
                "id": user_id,
                "email": email,
                "name": name,
                "hashed_password": hashed_password,
                "created_at": datetime.utcnow(),
                "tier": tier,
                "allowed_models": allowed_models
            }
            db.users.insert_one(new_user)
            print(f"Created new user '{email}' ({name}, ID: {user_id}) with {tier.capitalize()} tier.")

if __name__ == "__main__":
    create_gold_users()
