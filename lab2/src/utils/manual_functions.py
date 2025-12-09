"""
Regular functions for manual operations (no classes, no static methods)
All functions are regular functions that can be imported directly.
"""

# ====================== BASIC FUNCTIONS ======================

def manual_len(collection):
    """Manual implementation of len()"""
    if hasattr(collection, '__len__'):
        return collection.__len__()
    count = 0
    for _ in collection:
        count += 1
    return count

def manual_sum(numbers):
    """Manual implementation of sum()"""
    total = 0
    for num in numbers:
        total += num
    return total

def manual_max(numbers):
    """Manual implementation of max()"""
    if not numbers:
        return None
    max_val = numbers[0]
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def manual_min(numbers):
    """Manual implementation of min()"""
    if not numbers:
        return None
    min_val = numbers[0]
    for num in numbers:
        if num < min_val:
            min_val = num
    return min_val

def manual_abs(number):
    """Manual implementation of abs()"""
    if number < 0:
        return -number
    return number

def manual_round(number, decimals=0):
    """Manual implementation of round()"""
    multiplier = 10 ** decimals
    return manual_int(number * multiplier + 0.5) / multiplier

def manual_int(number):
    if isinstance(number, str):
        try:
            return int(float(number))
        except:
            return 0
    if number >= 0:
        return int(number // 1)  
    else:
        return -int(-number // 1) 

def manual_float(number):
    """Manual implementation of float()"""
    return number * 1.0

def manual_str(obj):
    if isinstance(obj, bool):
        return "True" if obj else "False"
    
    if isinstance(obj, str):
        return obj
    
    if isinstance(obj, (int, float)):
        return number_to_string(obj)
    try:
        return str(obj)
    except:
        return "[object]"
def number_to_string(number):
    """Convert number to string manually"""
    if number == 0:
        return "0"
    
    is_negative = number < 0
    if is_negative:
        number = -number
    integer_part = int(number // 1)
    decimal_part = number - integer_part
    int_str = ""
    temp = integer_part
    if temp == 0:
        int_str = "0"
    else:
        while temp > 0:
            digit = int(temp % 10)
            int_str = chr(ord('0') + digit) + int_str
            temp = int(temp // 10)
    if decimal_part > 0:
        int_str += "."
        decimal_as_int = int(round(decimal_part * 1000000))
        while decimal_as_int % 10 == 0 and decimal_as_int > 0:
            decimal_as_int //= 10
        if decimal_as_int > 0:
            temp_str = ""
            temp = decimal_as_int
            while temp > 0:
                digit = int(temp % 10)
                temp_str = chr(ord('0') + digit) + temp_str
                temp //= 10
            int_str += temp_str
    
    return ("-" if is_negative else "") + int_str

# ====================== COLLECTION FUNCTIONS ======================

def manual_list(iterable):
    """Manual implementation of list()"""
    result = []
    for item in iterable:
        result.append(item)
    return result

def manual_dict(keys_values):
    """Manual implementation of dict()"""
    result = {}
    for key, value in keys_values:
        result[key] = value
    return result

def manual_range(start, stop=None, step=1):
    """Manual implementation of range()"""
    if stop is None:
        stop = start
        start = 0
    
    result = []
    current = start
    while (step > 0 and current < stop) or (step < 0 and current > stop):
        result.append(current)
        current += step
    return result

def manual_zip(*iterables):
    """Manual implementation of zip()"""
    if not iterables:
        return []
    
    min_length = manual_min([manual_len(it) for it in iterables])
    result = []
    
    for i in manual_range(min_length):
        tuple_items = []
        for iterable in iterables:
            if isinstance(iterable, list):
                tuple_items.append(iterable[i])
            else:
                iterator = iter(iterable)
                for _ in manual_range(i + 1):
                    item = next(iterator)
                tuple_items.append(item)
        result.append(tuple(tuple_items))
    
    return result

def manual_enumerate(iterable, start=0):
    """Manual implementation of enumerate()"""
    result = []
    index = start
    for item in iterable:
        result.append((index, item))
        index += 1
    return result

def manual_sorted(iterable, reverse=False):
    """Manual implementation of sorted()"""
    arr = manual_list(iterable)
    n = manual_len(arr)
    
    for i in manual_range(n):
        for j in manual_range(0, n - i - 1):
            if (not reverse and arr[j] > arr[j + 1]) or (reverse and arr[j] < arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr

# ====================== HIGHER-ORDER FUNCTIONS ======================

def manual_filter(func, iterable):
    """Manual implementation of filter()"""
    result = []
    for item in iterable:
        if func(item):
            result.append(item)
    return result

def manual_map(func, iterable):
    """Manual implementation of map()"""
    result = []
    for item in iterable:
        result.append(func(item))
    return result

def manual_any(iterable):
    """Manual implementation of any()"""
    for item in iterable:
        if item:
            return True
    return False

def manual_all(iterable):
    """Manual implementation of all()"""
    for item in iterable:
        if not item:
            return False
    return True

def manual_join(strings, separator):
    """Manual implementation of str.join()"""
    if not strings:
        return ""
    result = strings[0]
    for i in manual_range(1, manual_len(strings)):
        result += separator + strings[i]
    return result

# ====================== ADDITIONAL CONVERSION FUNCTIONS ======================

def manual_int_convert(string):
    """Manual conversion of string to integer"""
    is_negative = False
    if string[0] == '-':
        is_negative = True
        string = string[1:]
    
    result = 0
    for char in string:
        result = result * 10 + (ord(char) - ord('0'))
    
    return -result if is_negative else result

def manual_float_convert(string):
    """Manual conversion of string to float"""
    is_negative = False
    if string[0] == '-':
        is_negative = True
        string = string[1:]
    
    parts = manual_split(string, '.')
    if manual_len(parts) == 1:
        integer_part = manual_int_convert(parts[0])
        return -integer_part if is_negative else integer_part
    else:
        integer_part = manual_int_convert(parts[0])
        decimal_part = manual_int_convert(parts[1])
        decimal_places = manual_len(parts[1])
        result = integer_part + decimal_part / (10 ** decimal_places)
        return -result if is_negative else result

def manual_split(string, delimiter):
    """Manual implementation of split()"""
    result = []
    current = ""
    for char in string:
        if char == delimiter:
            result.append(current)
            current = ""
        else:
            current += char
    result.append(current)
    return result