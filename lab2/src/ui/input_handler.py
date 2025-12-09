"""
Regular functions for input handling (no static methods, no decorators)
All functions use regular functions from utils
"""
from src.utils.manual_functions import manual_len, manual_int_convert, manual_float_convert
from src.utils.validation import validate_email_format, validate_phone_number

# ====================== PUBLIC INPUT FUNCTIONS ======================

def get_string_input(prompt, min_length=1, max_length=255):
    """Get string input from user with validation"""
    while True:
        try:
            print(prompt, end=": ")
            user_input = input().strip()
            
            input_length = manual_len(user_input)
            if input_length < min_length:
                print(f"Input must be at least {min_length} characters long.")
                continue
            
            if input_length > max_length:
                print(f"Input must be no more than {max_length} characters.")
                continue
            
            return user_input
            
        except EOFError:
            print("\nInput cancelled.")
            return None
        except Exception as e:
            print(f"Input error: {e}")

def get_integer_input(prompt, min_value=None, max_value=None):
    """Get integer input from user with validation"""
    while True:
        try:
            user_input = get_string_input(prompt)
            if user_input is None:
                return None
            
            if not is_integer_string(user_input):
                print("Please enter a valid integer.")
                continue
            
            number = manual_int_convert(user_input)
            
            if min_value is not None and number < min_value:
                print(f"Number must be at least {min_value}.")
                continue
            
            if max_value is not None and number > max_value:
                print(f"Number must be no more than {max_value}.")
                continue
            
            return number
            
        except Exception as e:
            print(f"Input error: {e}")

def get_float_input(prompt, min_value=None, max_value=None):
    """Get float input from user with validation"""
    while True:
        try:
            user_input = get_string_input(prompt)
            if user_input is None:
                return None

            if not is_float_string(user_input):
                print("Please enter a valid number.")
                continue
            
            number = manual_float_convert(user_input)
            
            if min_value is not None and number < min_value:
                print(f"Number must be at least {min_value}.")
                continue
            
            if max_value is not None and number > max_value:
                print(f"Number must be no more than {max_value}.")
                continue
            
            return number
            
        except Exception as e:
            print(f"Input error: {e}")

def get_email_input(prompt):
    """Get email input with validation"""
    while True:
        email = get_string_input(prompt, 5, 255)
        if email is None:
            return None
        
        if validate_email_format(email):
            return email
        else:
            print("Invalid email format. Please enter a valid email.")

def get_phone_input(prompt):
    """Get phone number input with validation"""
    while True:
        phone = get_string_input(prompt, 10, 15)
        if phone is None:
            return None
        
        if validate_phone_number(phone):
            return phone
        else:
            print("Invalid phone number. Please enter 10-15 digits.")

def get_choice_input(prompt, options):
    """Get choice from list of options"""
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        choice = get_integer_input("Enter your choice", 1, manual_len(options))
        if choice is None:
            return None
        
        return options[choice - 1]

def get_yes_no_input(prompt):
    """Get yes/no input"""
    while True:
        response = get_string_input(prompt + " (y/n)", 1, 1).lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

# ====================== HELPER FUNCTIONS ======================

def is_integer_string(string):
    """Check if string represents an integer"""
    if manual_len(string) == 0:
        return False
    
    if string[0] == '-':
        if manual_len(string) == 1:
            return False
        string = string[1:]
    
    for char in string:
        if not is_digit_character(char):
            return False
    return True

def is_float_string(string):
    """Check if string represents a float"""
    if manual_len(string) == 0:
        return False
    
    if string[0] == '-':
        if manual_len(string) == 1:
            return False
        string = string[1:]
    
    has_decimal = False
    for i, char in enumerate(string):
        if char == '.':
            if has_decimal or i == 0 or i == manual_len(string) - 1:
                return False
            has_decimal = True
        elif not is_digit_character(char):
            return False
    return True

def is_digit_character(char):
    """Check if character is a digit"""
    return '0' <= char <= '9'

class InputHandler:
    """Wrapper class for input functions"""
    
    def get_string_input(self, prompt, min_length=1, max_length=255):
        return get_string_input(prompt, min_length, max_length)
    
    def get_integer_input(self, prompt, min_value=None, max_value=None):
        return get_integer_input(prompt, min_value, max_value)
    
    def get_float_input(self, prompt, min_value=None, max_value=None):
        return get_float_input(prompt, min_value, max_value)
    
    def get_email_input(self, prompt):
        return get_email_input(prompt)
    
    def get_phone_input(self, prompt):
        return get_phone_input(prompt)
    
    def get_choice_input(self, prompt, options):
        return get_choice_input(prompt, options)
    
    def get_yes_no_input(self, prompt):
        return get_yes_no_input(prompt)

# Create instance
input_handler_instance = InputHandler()

# Ёкспортируем всЄ
__all__ = [
    'InputHandler',
    'input_handler_instance',
    'get_string_input',
    'get_integer_input',
    'get_float_input',
    'get_email_input',
    'get_phone_input',
    'get_choice_input',
    'get_yes_no_input',
    'is_integer_string',
    'is_float_string',
    'is_digit_character'
]