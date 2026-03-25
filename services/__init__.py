"""Business logic and database service layer"""
from .user_service import (
    get_next_user_id,
    email_exists,
    insert_user,
    get_user_by_id,
    get_all_users,
)
from .demand_service import (
    insert_demand,
    fetch_last_n_records,
    fetch_prev_day_demand,
    fetch_all_demand,
)
from .whatsapp_service import WhatsAppService

__all__ = [
    # User service
    "get_next_user_id",
    "email_exists",
    "insert_user",
    "get_user_by_id",
    "get_all_users",
    # Demand service
    "insert_demand",
    "fetch_last_n_records",
    "fetch_prev_day_demand",
    "fetch_all_demand",
    # WhatsApp service
    "WhatsAppService",
]
