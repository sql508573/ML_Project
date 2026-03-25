"""MongoDB client connection utility"""
from pymongo import MongoClient
from config.settings import MONGO_URI, DB_NAME


def get_db():
    """
    Get MongoDB database connection
    
    Returns:
        tuple: (client, database) MongoDB client and database instance
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return client, db
