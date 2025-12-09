import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rectangle import Rectangle, rectangle_from_string, create_rectangle_default

class TestRectangle(unittest.TestCase):

    def test_default_constructor(self):
        rect = Rectangle()
        self.assertEqual(rect.get_x(), 0)
        self.assertEqual(rect.get_y(), 0)
        self.assertEqual(rect.get_width(), 1)
        self.assertEqual(rect.get_height(), 1)

    def test_parameterized_constructor(self):
        rect = Rectangle(2, 3, 4, 5)
        self.assertEqual(rect.get_x(), 2)
        self.assertEqual(rect.get_y(), 3)
        self.assertEqual(rect.get_width(), 4)
        self.assertEqual(rect.get_height(), 5)

    def test_copy_constructor(self):
        rect1 = Rectangle(1, 2, 3, 4)
        rect2 = rect1.copy()
        self.assertEqual(rect1, rect2)
        self.assertIsNot(rect1, rect2)

    def test_negative_dimensions_normalization(self):
        rect = Rectangle(5, 5, -3, -2)
        self.assertEqual(rect.get_x(), 2)
        self.assertEqual(rect.get_y(), 3)
        self.assertEqual(rect.get_width(), 3)
        self.assertEqual(rect.get_height(), 2)

    def test_move_operation(self):
        rect = Rectangle(1, 1, 2, 2)
        rect.move(3, 4)
        self.assertEqual(rect.get_x(), 4)
        self.assertEqual(rect.get_y(), 5)

    def test_resize_operation(self):
        rect = Rectangle(1, 1, 2, 2)
        rect.resize(5, 6)
        self.assertEqual(rect.get_width(), 5)
        self.assertEqual(rect.get_height(), 6)

    def test_vertices_calculation(self):
        rect = Rectangle(1, 1, 3, 2)
        vertices = rect.get_vertices()
        expected_vertices = [(1, 1), (4, 1), (4, 3), (1, 3)]
        self.assertEqual(vertices, expected_vertices)

    def test_union_operation(self):
        rect1 = Rectangle(0, 0, 2, 2)
        rect2 = Rectangle(1, 1, 2, 2)
        union_rect = rect1 + rect2
        self.assertEqual(union_rect.get_x(), 0)
        self.assertEqual(union_rect.get_y(), 0)
        self.assertEqual(union_rect.get_width(), 3)
        self.assertEqual(union_rect.get_height(), 3)

    def test_intersection_operation(self):
        rect1 = Rectangle(0, 0, 3, 3)
        rect2 = Rectangle(1, 1, 3, 3)
        intersection_rect = rect1 - rect2
        self.assertEqual(intersection_rect.get_x(), 1)
        self.assertEqual(intersection_rect.get_y(), 1)
        self.assertEqual(intersection_rect.get_width(), 2)
        self.assertEqual(intersection_rect.get_height(), 2)

    def test_empty_intersection(self):
        rect1 = Rectangle(0, 0, 1, 1)
        rect2 = Rectangle(2, 2, 1, 1)
        intersection_rect = rect1 - rect2
        self.assertEqual(intersection_rect.get_x(), 0)
        self.assertEqual(intersection_rect.get_y(), 0)
        self.assertEqual(intersection_rect.get_width(), 1)
        self.assertEqual(intersection_rect.get_height(), 1)

    def test_comparison_operators(self):
        rect1 = Rectangle(1, 1, 2, 2)
        rect2 = Rectangle(1, 1, 2, 2)
        rect3 = Rectangle(2, 2, 3, 3)

        self.assertEqual(rect1, rect2)
        self.assertNotEqual(rect1, rect3)

    def test_increment_decrement_operators(self):
        rect = Rectangle(1, 1, 2, 2)
        rect_inc = +rect
        self.assertEqual(rect_inc.get_width(), 3)
        self.assertEqual(rect_inc.get_height(), 3)
        rect_dec = -rect
        self.assertEqual(rect_dec.get_width(), 1)
        self.assertEqual(rect_dec.get_height(), 1)

    def test_in_place_union(self):
        rect1 = Rectangle(0, 0, 2, 2)
        rect2 = Rectangle(1, 1, 2, 2)
        rect1 += rect2
        self.assertEqual(rect1.get_width(), 3)
        self.assertEqual(rect1.get_height(), 3)

    def test_in_place_intersection(self):
        rect1 = Rectangle(0, 0, 3, 3)
        rect2 = Rectangle(1, 1, 2, 2)
        rect1 -= rect2
        self.assertEqual(rect1.get_x(), 1)
        self.assertEqual(rect1.get_y(), 1)

    def test_string_operations(self):
        rect = Rectangle(1, 2, 3, 4)
        str_repr = rect.to_string()
        
        # Используем функцию-помощник вместо classmethod
        rect_parsed = rectangle_from_string(str_repr)
        
        self.assertEqual(rect, rect_parsed)

    def test_string_representation(self):
        rect = Rectangle(1, 2, 3, 4)
        str_repr = str(rect)
        self.assertIn("x=1", str_repr)
        self.assertIn("y=2", str_repr)
        self.assertIn("width=3", str_repr)
        self.assertIn("height=4", str_repr)

    def test_edge_case_zero_dimensions(self):
        rect = Rectangle(0, 0, 0, 0)
        self.assertEqual(rect.get_width(), 0)
        self.assertEqual(rect.get_height(), 0)

    # Новые тесты для проверки новых методов
    def test_from_string_as_instance_method(self):
        """Test from_string as instance method"""
        rect = Rectangle(0, 0, 1, 1)
        rect2 = rect.from_string("1 2 3 4")
        self.assertEqual(rect2.get_x(), 1)
        self.assertEqual(rect2.get_y(), 2)
        self.assertEqual(rect2.get_width(), 3)
        self.assertEqual(rect2.get_height(), 4)

    def test_create_from_string_method(self):
        """Test create_from_string method"""
        rect = Rectangle(0, 0, 1, 1)
        rect2 = rect.create_from_string("5 6 7 8")
        self.assertEqual(rect2.get_x(), 5)
        self.assertEqual(rect2.get_y(), 6)
        self.assertEqual(rect2.get_width(), 7)
        self.assertEqual(rect2.get_height(), 8)

    def test_rectangle_from_string_function(self):
        """Test rectangle_from_string helper function"""
        rect = rectangle_from_string("10 20 30 40")
        self.assertEqual(rect.get_x(), 10)
        self.assertEqual(rect.get_y(), 20)
        self.assertEqual(rect.get_width(), 30)
        self.assertEqual(rect.get_height(), 40)

class TestRectangleAdvanced(unittest.TestCase):

    def test_large_coordinates(self):
        rect = Rectangle(1000, 1000, 5000, 5000)
        self.assertEqual(rect.get_x(), 1000)
        self.assertEqual(rect.get_width(), 5000)

    def test_negative_coordinates(self):
        rect = Rectangle(-10, -20, 5, 5)
        self.assertEqual(rect.get_x(), -10)
        self.assertEqual(rect.get_y(), -20)

    def test_associative_property(self):
        rect1 = Rectangle(0, 0, 2, 2)
        rect2 = Rectangle(1, 1, 2, 2)
        rect3 = Rectangle(2, 2, 2, 2)

        union1 = (rect1 + rect2) + rect3
        union2 = rect1 + (rect2 + rect3)
        self.assertEqual(union1, union2)

if __name__ == '__main__':
    unittest.main(verbosity=2)