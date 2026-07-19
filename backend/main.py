import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.database import init_db
from backend.routers import chat, sessions, auth
from backend.utils.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zydrakon AI Chatbot API",
    description="FastAPI Backend for Zydrakon AI chatbot powered by OpenRouter",
    version="1.0.0"
)

import os

cors_origins_str = os.getenv("FRONTEND_URL", "http://localhost:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(sessions.router)

@app.on_event("startup")
def startup_event():
    logger.info("Initializing Zydrakon AI Database...")
    init_db()
    logger.info("Zydrakon AI Database initialized successfully!")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Zydrakon AI Chatbot API",
        "description": "FastAPI Backend is running and ready to handle chat requests."
    }
