import re
from datetime import datetime

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    # Validación simple de teléfono
    pattern = r'^[\+]?[0-9\s\-\(\)]{10,}$'
    return re.match(pattern, phone) is not None

def validate_appointment_time(start_time: datetime, end_time: datetime) -> bool:
    return start_time < end_time

def validate_budget_range(min_budget: float, max_budget: float) -> bool:
    return min_budget <= max_budget and min_budget >= 0
