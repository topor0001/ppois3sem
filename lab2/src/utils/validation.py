"""
Regular validation functions (no classes, no static methods)
All functions are regular functions that can be imported directly.
"""
from src.utils.manual_functions import manual_len
from src.constants.validation_constants import ValidationConstants
from src.constants.financial_constants import FinancialConstants
from src.constants.config_constants import ConfigConstants

# ====================== VALIDATION FUNCTIONS ======================

def validate_email_format(email):
    # Basic email validation
    if not email or '@' not in email:
        return False
    
    # Разделяем email на локальную часть и домен
    parts = email.split('@')
    if len(parts) != 2:
        return False
    
    local_part, domain_part = parts
    
    # Проверяем, что локальная часть не пустая
    if not local_part or local_part.strip() == '':
        return False
    
    # Проверяем, что доменная часть не пустая
    if not domain_part or domain_part.strip() == '':
        return False
    
    # Проверяем, что в доменной части есть точка
    if '.' not in domain_part:
        return False
    
    # Проверяем, что после последней точки есть минимум 2 символа
    domain_parts = domain_part.split('.')
    if len(domain_parts[-1]) < 2:
        return False
    
    # Базовая проверка на пробелы
    if ' ' in email:
        return False
    
    return True

def validate_phone_number(phone_number):
    """Validate phone number format"""
  
    
    phone_length = manual_len(phone_number)
    if phone_length < ValidationConstants.MIN_PHONE_LENGTH:
        return False
    if phone_length > ValidationConstants.MAX_PHONE_LENGTH:
        return False
    
    digit_counter = 0
    for character in phone_number:
        if character.isdigit():
            digit_counter += 1
    
    return digit_counter >= 10

def validate_price_value(price_amount):
    """Validate price amount is within valid range"""
   
    
    return (price_amount >= FinancialConstants.MIN_PAYMENT_AMOUNT and 
            price_amount <= FinancialConstants.MAX_PAYMENT_AMOUNT)

def validate_quantity_amount(quantity_amount):
    """Validate quantity amount is within valid range"""

    
    return (quantity_amount >= 0 and 
            quantity_amount <= ConfigConstants.MAX_PARTS_QUANTITY)

def validate_date_format(date_string):
    """Validate date string format (YYYY-MM-DD)"""
    date_length = manual_len(date_string)
    if date_length != 10:
        return False
    
    if date_string[4] != '-' or date_string[7] != '-':
        return False
    
    year_part = date_string[0:4]
    month_part = date_string[5:7]
    day_part = date_string[8:10]
    
    for date_part in [year_part, month_part, day_part]:
        for character in date_part:
            if not character.isdigit():
                return False
    
    try:
        year_value = int(year_part)
        month_value = int(month_part)
        day_value = int(day_part)
    except ValueError:
        return False
    
    return (1 <= month_value <= 12 and 1 <= day_value <= 31 and year_value >= 2000)

# ====================== COMPATIBILITY FUNCTIONS ======================

def validate_email_format_legacy(email_address):
    """Legacy name for validate_email_format (for compatibility)"""
    return validate_email_format(email_address)

def validate_phone_number_legacy(phone_number):
    """Legacy name for validate_phone_number (for compatibility)"""
    return validate_phone_number(phone_number)

def validate_price_value_legacy(price_amount):
    """Legacy name for validate_price_value (for compatibility)"""
    return validate_price_value(price_amount)

def validate_quantity_amount_legacy(quantity_amount):
    """Legacy name for validate_quantity_amount (for compatibility)"""
    return validate_quantity_amount(quantity_amount)

def validate_date_format_legacy(date_string):
    """Legacy name for validate_date_format (for compatibility)"""
    return validate_date_format(date_string)