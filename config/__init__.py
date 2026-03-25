"""Configuration settings for the ML project"""
from .settings import (
    MONGO_URI,
    DB_NAME,
    USERS_COLLECTION,
    DEMAND_COLLECTION,
    MODELS_DIR,
    FEATURE_COLS,
    TARGET_COL,
)

__all__ = [
    "MONGO_URI",
    "DB_NAME",
    "USERS_COLLECTION",
    "DEMAND_COLLECTION",
    "MODELS_DIR",
    "FEATURE_COLS",
    "TARGET_COL",
]
