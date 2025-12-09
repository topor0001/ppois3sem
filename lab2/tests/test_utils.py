import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils import manual_utils_instance as ManualUtils
from src.utils.validation import (
    validate_email_format, validate_phone_number, 
    validate_price_value, validate_quantity_amount, 
    validate_date_format
)
from src.utils.manual_functions import (
    manual_int, manual_float, manual_str, number_to_string,
    manual_list, manual_dict, manual_int_convert,
    manual_float_convert, manual_split
)

class TestManualFunctions(unittest.TestCase):
    def test_manual_len(self):
        self.assertEqual(ManualUtils.manual_len([1, 2, 3]), 3)
        self.assertEqual(ManualUtils.manual_len("hello"), 5)
        self.assertEqual(ManualUtils.manual_len([]), 0)

    def test_manual_sum(self):
        self.assertEqual(ManualUtils.manual_sum([1, 2, 3, 4]), 10)
        self.assertEqual(ManualUtils.manual_sum([]), 0)
        self.assertEqual(ManualUtils.manual_sum([-1, 0, 1]), 0)

    def test_manual_max(self):
        self.assertEqual(ManualUtils.manual_max([3, 1, 4, 2]), 4)
        self.assertEqual(ManualUtils.manual_max([-5, -2, -10]), -2)
        self.assertIsNone(ManualUtils.manual_max([]))

    def test_manual_min(self):
        self.assertEqual(ManualUtils.manual_min([3, 1, 4, 2]), 1)
        self.assertEqual(ManualUtils.manual_min([-5, -2, -10]), -10)
        self.assertIsNone(ManualUtils.manual_min([]))

    def test_manual_abs(self):
        self.assertEqual(ManualUtils.manual_abs(-5), 5)
        self.assertEqual(ManualUtils.manual_abs(5), 5)
        self.assertEqual(ManualUtils.manual_abs(0), 0)

    def test_manual_round(self):
        self.assertEqual(ManualUtils.manual_round(3.14159, 2), 3.14)
        self.assertEqual(ManualUtils.manual_round(2.5), 3)
        self.assertEqual(ManualUtils.manual_round(2.4), 2)

    def test_manual_range(self):
        self.assertEqual(ManualUtils.manual_range(5), [0, 1, 2, 3, 4])
        self.assertEqual(ManualUtils.manual_range(2, 6), [2, 3, 4, 5])
        self.assertEqual(ManualUtils.manual_range(1, 10, 2), [1, 3, 5, 7, 9])

    def test_manual_zip(self):
        result = ManualUtils.manual_zip([1, 2, 3], ['a', 'b', 'c'])
        self.assertEqual(result, [(1, 'a'), (2, 'b'), (3, 'c')])

    def test_manual_enumerate(self):
        result = ManualUtils.manual_enumerate(['a', 'b', 'c'])
        self.assertEqual(result, [(0, 'a'), (1, 'b'), (2, 'c')])

    def test_manual_sorted(self):
        self.assertEqual(ManualUtils.manual_sorted([3, 1, 4, 2]), [1, 2, 3, 4])
        self.assertEqual(ManualUtils.manual_sorted([3, 1, 4, 2], reverse=True), [4, 3, 2, 1])

    def test_manual_filter(self):
        result = ManualUtils.manual_filter(lambda x: x > 2, [1, 2, 3, 4])
        self.assertEqual(result, [3, 4])

    def test_manual_map(self):
        result = ManualUtils.manual_map(lambda x: x * 2, [1, 2, 3])
        self.assertEqual(result, [2, 4, 6])

    def test_manual_any(self):
        self.assertTrue(ManualUtils.manual_any([False, True, False]))
        self.assertFalse(ManualUtils.manual_any([False, False, False]))

    def test_manual_all(self):
        self.assertTrue(ManualUtils.manual_all([True, True, True]))
        self.assertFalse(ManualUtils.manual_all([True, False, True]))

    def test_manual_join(self):
        result = ManualUtils.manual_join(['a', 'b', 'c'], ', ')
        self.assertEqual(result, "a, b, c")

class TestDataValidator(unittest.TestCase):
    def test_email_validation(self):
        self.assertTrue(validate_email_format("test@example.com"))
        self.assertTrue(validate_email_format("user.name@domain.co.uk"))
        self.assertFalse(validate_email_format("invalid-email"))
        self.assertFalse(validate_email_format("user@"))
        self.assertFalse(validate_email_format("@domain.com"))

    def test_phone_validation(self):
        self.assertTrue(validate_phone_number("+1234567890"))
        self.assertTrue(validate_phone_number("1234567890"))
        self.assertFalse(validate_phone_number("123"))
        self.assertFalse(validate_phone_number("abc"))
        self.assertFalse(validate_phone_number("123-456-789"))

    def test_price_validation(self):
        self.assertTrue(validate_price_value(50.0))
        self.assertTrue(validate_price_value(1.0))
        self.assertFalse(validate_price_value(-10.0))
        self.assertFalse(validate_price_value(0.0))

    def test_quantity_validation(self):
        self.assertTrue(validate_quantity_amount(10))
        self.assertTrue(validate_quantity_amount(0))
        self.assertFalse(validate_quantity_amount(-5))

    def test_date_validation(self):
        self.assertTrue(validate_date_format("2024-01-15"))
        self.assertTrue(validate_date_format("2024-12-31"))
        self.assertFalse(validate_date_format("2024/01/15"))
        self.assertFalse(validate_date_format("24-01-15"))
        self.assertFalse(validate_date_format("invalid-date"))

class TestManualFunctionsExtended(unittest.TestCase):
    
    def test_manual_int(self):
        self.assertEqual(manual_int(5.7), 5)
        self.assertEqual(manual_int(10.2), 10)
        self.assertEqual(manual_int(-3.8), -3)
        self.assertEqual(manual_int(0.0), 0)
    
    def test_manual_float(self):
        self.assertEqual(manual_float(5), 5.0)
        self.assertEqual(manual_float(-3), -3.0)
        self.assertEqual(manual_float(0), 0.0)
    
    def test_manual_str(self):
        self.assertEqual(manual_str("hello"), "hello")
        self.assertEqual(manual_str(123), "123")
        self.assertEqual(manual_str(45.67), "45.67")
        self.assertEqual(manual_str(True), "True")
        self.assertEqual(manual_str(False), "False")
    
    def test_number_to_string(self):
        self.assertEqual(number_to_string(0), "0")
        self.assertEqual(number_to_string(123), "123")
        self.assertEqual(number_to_string(-456), "-456")
        self.assertEqual(number_to_string(3.14), "3.14")
        self.assertEqual(number_to_string(-2.5), "-2.5")
    
    def test_manual_list(self):
        self.assertEqual(manual_list([1, 2, 3]), [1, 2, 3])
        self.assertEqual(manual_list("abc"), ["a", "b", "c"])
        self.assertEqual(manual_list(range(3)), [0, 1, 2])
        self.assertEqual(manual_list([]), [])
    
    def test_manual_dict(self):
        items = [("a", 1), ("b", 2), ("c", 3)]
        self.assertEqual(manual_dict(items), {"a": 1, "b": 2, "c": 3})
        empty_items = []
        self.assertEqual(manual_dict(empty_items), {})
    
    def test_manual_int_convert(self):
        self.assertEqual(manual_int_convert("123"), 123)
        self.assertEqual(manual_int_convert("-456"), -456)
        self.assertEqual(manual_int_convert("0"), 0)
        with self.assertRaises(Exception):
            manual_int_convert("")
    
    def test_manual_float_convert(self):
        self.assertEqual(manual_float_convert("123.45"), 123.45)
        self.assertEqual(manual_float_convert("-78.9"), -78.9)
        self.assertEqual(manual_float_convert("0.0"), 0.0)
        self.assertEqual(manual_float_convert("100"), 100.0)
    
    def test_manual_split(self):
        self.assertEqual(manual_split("a,b,c", ","), ["a", "b", "c"])
        self.assertEqual(manual_split("hello world", " "), ["hello", "world"])
        self.assertEqual(manual_split("test", ","), ["test"])
        self.assertEqual(manual_split("", ","), [""])

if __name__ == '__main__':
    unittest.main()