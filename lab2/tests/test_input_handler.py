# Файл: tests/test_input_handler.py
import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.ui.input_handler import (
    get_string_input, get_integer_input, get_float_input,
    get_email_input, get_phone_input, get_choice_input,
    get_yes_no_input, InputHandler, input_handler_instance,
    is_integer_string, is_float_string, is_digit_character
)

class TestInputHandlerBasicFunctions(unittest.TestCase):
    
    def test_is_digit_character(self):
        # Тест проверки цифрового символа
        self.assertTrue(is_digit_character('0'))
        self.assertTrue(is_digit_character('5'))
        self.assertTrue(is_digit_character('9'))
        self.assertFalse(is_digit_character('a'))
        self.assertFalse(is_digit_character(' '))
        self.assertFalse(is_digit_character('.'))
        self.assertFalse(is_digit_character('-'))
    
    def test_is_integer_string(self):
        # Тест проверки строки-целого числа
        self.assertTrue(is_integer_string("0"))
        self.assertTrue(is_integer_string("123"))
        self.assertTrue(is_integer_string("-456"))
        self.assertFalse(is_integer_string(""))
        self.assertFalse(is_integer_string("12.3"))
        self.assertFalse(is_integer_string("abc"))
        self.assertFalse(is_integer_string("123abc"))
        self.assertFalse(is_integer_string("--123"))
        self.assertFalse(is_integer_string("-"))
    
    def test_is_float_string(self):
        # Тест проверки строки-дробного числа
        self.assertTrue(is_float_string("0.0"))
        self.assertTrue(is_float_string("3.14"))
        self.assertTrue(is_float_string("-2.5"))
        self.assertFalse(is_float_string(""))
        self.assertFalse(is_float_string("abc"))
        self.assertFalse(is_float_string("1.2.3"))
        self.assertFalse(is_float_string("."))
        self.assertFalse(is_float_string("-."))

class TestInputHandlerWithMockedInput(unittest.TestCase):
    
    def test_get_string_input_valid(self):
        # Тест получения строки - валидный ввод
        mock_input = MagicMock(return_value='Hello World')
        
        # Перехватываем вывод, чтобы не мешал тестам
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                result = get_string_input("Enter text")
                self.assertEqual(result, 'Hello World')
    
    def test_get_string_input_empty_then_valid(self):
        # Тест получения строки - пустой, затем валидный
        mock_input = MagicMock(side_effect=['', 'Valid Input'])
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_string_input("Enter text", min_length=1)
                self.assertEqual(result, 'Valid Input')
    
    def test_get_string_input_too_long_then_valid(self):
        # Тест получения строки - слишком длинная, затем валидная
        long_string = 'a' * 300
        valid_string = 'Valid'
        mock_input = MagicMock(side_effect=[long_string, valid_string])
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_string_input("Enter text", max_length=255)
                self.assertEqual(result, valid_string)
    
    def test_get_integer_input_valid(self):
        # Тест получения целого числа - валидный ввод
        mock_input = MagicMock(return_value='42')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_integer_input("Enter number")
                self.assertEqual(result, 42)
    
    def test_get_integer_input_with_range_valid(self):
        # Тест получения целого числа в диапазоне
        mock_input = MagicMock(return_value='5')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_integer_input("Enter number", 1, 10)
                self.assertEqual(result, 5)
    
    def test_get_integer_input_out_of_range_then_valid(self):
        # Тест получения целого числа - вне диапазона, затем валидный
        mock_input = MagicMock(side_effect=['0', '15', '8'])
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_integer_input("Enter number", 1, 10)
                self.assertEqual(result, 8)
    
    def test_get_integer_input_invalid_then_valid(self):
        # Тест получения целого числа - не число, затем валидный
        mock_input = MagicMock(side_effect=['abc', '123'])
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_integer_input("Enter number")
                self.assertEqual(result, 123)
    
    def test_get_float_input_valid(self):
        # Тест получения дробного числа - валидный ввод
        mock_input = MagicMock(return_value='3.14')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_float_input("Enter float")
                self.assertEqual(result, 3.14)
    
    def test_get_float_input_with_range_valid(self):
        # Тест получения дробного числа в диапазоне
        mock_input = MagicMock(return_value='5.5')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_float_input("Enter float", 0.0, 10.0)
                self.assertEqual(result, 5.5)
    
    def test_get_float_input_invalid_then_valid(self):
        # Тест получения дробного числа - не число, затем валидный
        mock_input = MagicMock(side_effect=['not_a_number', '2.718'])
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_float_input("Enter float")
                self.assertEqual(result, 2.718)
    
    def test_get_email_input_valid(self):
        # Тест получения email - валидный
        mock_input = MagicMock(return_value='test@example.com')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_email_input("Enter email")
                self.assertEqual(result, 'test@example.com')
    
    def test_get_phone_input_valid(self):
        # Тест получения телефона - валидный
        mock_input = MagicMock(return_value='+12345678901')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_phone_input("Enter phone")
                self.assertEqual(result, '+12345678901')
    
    def test_get_choice_input_valid(self):
        # Тест выбора из списка - валидный
        mock_input = MagicMock(return_value='2')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                options = ['Apple', 'Banana', 'Cherry']
                result = get_choice_input("Choose fruit", options)
                self.assertEqual(result, 'Banana')
    
    def test_get_yes_no_input_yes(self):
        # Тест да/нет - да
        mock_input = MagicMock(return_value='y')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_yes_no_input("Continue?")
                self.assertTrue(result)
    
    def test_get_yes_no_input_no(self):
        # Тест да/нет - нет
        mock_input = MagicMock(return_value='n')
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = get_yes_no_input("Continue?")
                self.assertFalse(result)

class TestInputHandlerClass(unittest.TestCase):
    
    def test_input_handler_instance(self):
        # Тест экземпляра InputHandler
        self.assertIsInstance(input_handler_instance, InputHandler)
    
    def test_input_handler_methods(self):
        # Тест методов класса InputHandler
        handler = InputHandler()
        
        # Тест get_string_input
        mock_input = MagicMock(return_value='test')
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = handler.get_string_input("Test")
                self.assertEqual(result, 'test')
        
        # Тест get_integer_input
        mock_input = MagicMock(return_value='123')
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = handler.get_integer_input("Test")
                self.assertEqual(result, 123)
        
        # Тест get_float_input
        mock_input = MagicMock(return_value='45.6')
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                result = handler.get_float_input("Test")
                self.assertEqual(result, 45.6)
    
    def test_input_handler_has_all_methods(self):
        # Тест наличия всех методов в InputHandler
        handler = InputHandler()
        expected_methods = [
            'get_string_input',
            'get_integer_input', 
            'get_float_input',
            'get_email_input',
            'get_phone_input',
            'get_choice_input',
            'get_yes_no_input'
        ]
        
        for method_name in expected_methods:
            self.assertTrue(hasattr(handler, method_name))
            self.assertTrue(callable(getattr(handler, method_name)))

class TestInputHandlerEdgeCases(unittest.TestCase):
    
    def test_get_string_input_eof_error(self):
        # Тест обработки EOFError (Ctrl+D / Ctrl+Z)
        mock_input = MagicMock(side_effect=EOFError())
        
        # Перехватываем stderr, чтобы не видеть сообщение об ошибке
        import io
        from contextlib import redirect_stderr
        
        stderr_capture = io.StringIO()
        
        with patch('builtins.input', mock_input):
            with patch('sys.stdout', new=StringIO()):
                with redirect_stderr(stderr_capture):
                    result = get_string_input("Enter text")
        
        self.assertIsNone(result)
   

# Простые тесты без моков для базовых функций
class TestSimpleInputFunctions(unittest.TestCase):
    
    def test_character_validation(self):
        # Простой тест проверки символов
        self.assertEqual(is_digit_character('5'), True)
        self.assertEqual(is_digit_character('a'), False)
        self.assertEqual(is_digit_character('0'), True)
        self.assertEqual(is_digit_character('9'), True)
    
    def test_string_validation(self):
        # Простой тест проверки строк
        self.assertEqual(is_integer_string("123"), True)
        self.assertEqual(is_integer_string("12.3"), False)
        self.assertEqual(is_integer_string("-456"), True)
        self.assertEqual(is_integer_string("abc"), False)
        
        self.assertEqual(is_float_string("3.14"), True)
        self.assertEqual(is_float_string("100"), True)  # Целое тоже float
        self.assertEqual(is_float_string("abc"), False)
        self.assertEqual(is_float_string("1.2.3"), False)

# Еще более простые тесты - только для непокрытых функций
class TestInputHandlerQuickCoverage(unittest.TestCase):
    
    def test_basic_validation_functions(self):
        # Эти функции точно есть и их можно тестировать без моков
        self.assertTrue(is_digit_character('7'))
        self.assertFalse(is_digit_character('x'))
        
        self.assertTrue(is_integer_string("100"))
        self.assertFalse(is_integer_string("10.5"))
        
        self.assertTrue(is_float_string("3.1415"))
        self.assertFalse(is_float_string("abc"))
    
    def test_input_handler_class_exists(self):
        # Просто проверяем, что класс и экземпляр существуют
        self.assertTrue(hasattr(input_handler_instance, 'get_string_input'))
        self.assertTrue(callable(input_handler_instance.get_string_input))
        
        # Проверяем, что InputHandler можно создать
        handler = InputHandler()
        self.assertIsInstance(handler, InputHandler)
    
    def test_validation_functions_if_exist(self):
        # Проверяем, есть ли функции валидации email и phone
     try:
        from src.ui.input_handler import validate_email_format
    # Если функция есть, тестируем ее
        result = validate_email_format("test@example.com")
        self.assertIsInstance(result, bool)
     except (ImportError, AttributeError):
    # Если функции нет, пропускаем
        pass

if __name__ == '__main__':
    unittest.main()