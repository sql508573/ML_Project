"""Input validation utilities"""
import re


def validate_email(email):
    """
    Validate email format
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid email format
    """
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    Validate phone number (10 digits)
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid 10-digit phone number
    """
    pattern = r"^\d{10}$"
    return bool(re.match(pattern, phone))


def validate_numeric(value, allow_float=False):
    """
    Validate numeric input
    
    Args:
        value (str): Value to validate
        allow_float (bool): Whether to allow floating point numbers
        
    Returns:
        tuple: (is_valid, converted_value)
    """
    try:
        if allow_float:
            return True, float(value)
        else:
            return True, int(value)
    except (ValueError, TypeError):
        return False, None


def validate_user_input(data):
    """
    Validate user registration data
    
    Args:
        data (dict): Dictionary with keys: name, email, phone, age, 
                     base_daily_demand_kg, restaurant_sales_share
                     
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    if not data.get("name") or not data.get("location"):
        errors.append("Name and location cannot be empty.")
    
    if not validate_email(data.get("email", "")):
        errors.append("Invalid email format.")
    
    if not validate_phone(data.get("phone", "")):
        errors.append("Invalid phone number. Must be 10 digits.")
    
    is_valid, _ = validate_numeric(data.get("age", ""), allow_float=False)
    if not is_valid:
        errors.append("Age must be a number.")
    
    is_valid, _ = validate_numeric(data.get("base_daily_demand_kg", ""), allow_float=True)
    if not is_valid:
        errors.append("Baseline demand must be a number.")
    
    is_valid, share = validate_numeric(data.get("restaurant_sales_share", ""), allow_float=True)
    if not is_valid:
        errors.append("Restaurant share must be a number.")
    elif not (0 <= share <= 1):
        errors.append("Restaurant share must be between 0 and 1.")
    
    return len(errors) == 0, errors
