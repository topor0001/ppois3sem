import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from set import Set, set_from_string, create_empty_set, create_set_from_elements

def create_unique_set():
    return Set()

class TestSet(unittest.TestCase):

    def test_default_constructor(self):
        test_set = Set()
        self.assertTrue(test_set.is_empty())
        self.assertEqual(test_set.get_cardinality(), 0)

    def test_constructor_with_elements(self):
        element1 = create_unique_set()
        element2 = create_unique_set()
        test_set = Set([element1, element2])
        self.assertEqual(test_set.get_cardinality(), 2)

    def test_copy_functionality(self):
        set1 = Set()
        element = create_unique_set()
        set1.add_element(element)
        set2 = set1.copy()
        self.assertEqual(set1, set2)
        self.assertIsNot(set1, set2)

    def test_add_remove_elements(self):
        test_set = Set()
        element1 = create_unique_set()
        element2 = create_unique_set()
        test_set.add_element(element1)
        self.assertEqual(test_set.get_cardinality(), 1)
        test_set.add_element(element2)
        self.assertEqual(test_set.get_cardinality(), 2)
        test_set.remove_element(element1)
        self.assertEqual(test_set.get_cardinality(), 1)

    def test_add_duplicate_elements(self):
        test_set = Set()
        element = create_unique_set()
        test_set.add_element(element)
        test_set.add_element(element)
        self.assertEqual(test_set.get_cardinality(), 1)

    def test_contains_operator(self):
        test_set = Set()
        element = create_unique_set()
        self.assertNotIn(element, test_set)
        test_set.add_element(element)
        self.assertIn(element, test_set)

    def test_element_access_operator(self):
        test_set = Set()
        element = create_unique_set()
        self.assertFalse(test_set[element])
        test_set.add_element(element)
        self.assertTrue(test_set[element])

    def test_union_operation(self):
        set1 = Set()
        set2 = Set()
        element1 = create_unique_set()
        element2 = create_unique_set()
        set1.add_element(element1)
        set2.add_element(element2)
        union_set = set1 + set2
        self.assertEqual(union_set.get_cardinality(), 2)

    def test_intersection_operation(self):
        set1 = Set()
        set2 = Set()
        common_element = create_unique_set()
        set1.add_element(common_element)
        set2.add_element(common_element)
        intersection_set = set1 * set2
        self.assertEqual(intersection_set.get_cardinality(), 1)

    def test_empty_intersection(self):
        set1 = Set()
        set2 = Set()
        element1 = create_unique_set()
        element2 = create_unique_set()
        set1.add_element(element1)
        set2.add_element(element2)
        intersection_set = set1 * set2
        self.assertEqual(intersection_set.get_cardinality(), 0)

    def test_difference_operation(self):
        set1 = Set()
        set2 = Set()
        element1 = create_unique_set()
        element2 = create_unique_set()
        set1.add_element(element1)
        set1.add_element(element2)
        set2.add_element(element1)
        difference_set = set1 - set2
        self.assertEqual(difference_set.get_cardinality(), 1)

    def test_in_place_operations(self):
        set1 = Set()
        set2 = Set()
        element1 = create_unique_set()
        element2 = create_unique_set()
        set1.add_element(element1)
        set2.add_element(element2)
        set1 += set2
        self.assertEqual(set1.get_cardinality(), 2)
        intersection_set = Set([element2])
        set1 *= intersection_set
        self.assertEqual(set1.get_cardinality(), 1)
        difference_set = Set([element2])
        set1 -= difference_set
        self.assertEqual(set1.get_cardinality(), 0)

    def test_power_set_empty(self):
        test_set = Set()
        power_set = test_set.get_power_set()
        self.assertEqual(power_set.get_cardinality(), 1)

    def test_power_set_one_element(self):
        test_set = Set()
        element = create_unique_set()
        test_set.add_element(element)
        power_set = test_set.get_power_set()
        self.assertEqual(power_set.get_cardinality(), 2)

    def test_power_set_two_elements(self):
        test_set = Set()
        element1 = create_unique_set()
        element2 = create_unique_set()
        test_set.add_element(element1)
        test_set.add_element(element2)
        power_set = test_set.get_power_set()
        self.assertEqual(power_set.get_cardinality(), 4)

    def test_comparison_operators(self):
        set1 = Set()
        set2 = Set()
        element = create_unique_set()
        set1.add_element(element)
        set2.add_element(element)
        self.assertEqual(set1, set2)
        set3 = Set()
        different_element = create_unique_set()
        set3.add_element(different_element)
        self.assertNotEqual(set1, set3)

    def test_string_representation(self):
        test_set = Set()
        self.assertEqual(str(test_set), "{}")
        element = create_unique_set()
        test_set.add_element(element)
        self.assertTrue(str(test_set).startswith("{"))
        self.assertTrue(str(test_set).endswith("}"))

    def test_from_string_empty(self):
        # Используем функцию-помощник вместо classmethod
        test_set = set_from_string("{}")
        self.assertTrue(test_set.is_empty())

    def test_iterator(self):
        test_set = Set()
        element1 = create_unique_set()
        element2 = create_unique_set()
        test_set.add_element(element1)
        test_set.add_element(element2)
        elements = list(test_set)
        self.assertEqual(len(elements), 2)

    def test_length_operator(self):
        test_set = Set()
        self.assertEqual(len(test_set), 0)
        test_set.add_element(create_unique_set())
        self.assertEqual(len(test_set), 1)

    # Новые тесты для новых методов
    def test_from_string_as_instance_method(self):
        """Test from_string as instance method"""
        test_set = Set()
        result = test_set.from_string("{1, 2, 3}")
        self.assertEqual(result.get_cardinality(), 3)

    def test_parse_string_method(self):
        """Test parse_string method"""
        test_set = Set()
        result = test_set.parse_string("{a, b, c}")
        self.assertEqual(result.get_cardinality(), 3)

    def test_set_from_string_function(self):
        """Test set_from_string helper function"""
        result = set_from_string("{1, 2, 3, 4}")
        self.assertEqual(result.get_cardinality(), 4)

    def test_create_empty_set_function(self):
        """Test create_empty_set function"""
        result = create_empty_set()
        self.assertTrue(result.is_empty())
        self.assertEqual(result.get_cardinality(), 0)

    def test_create_set_from_elements_function(self):
        """Test create_set_from_elements function"""
        elements = [1, 2, 3]
        result = create_set_from_elements(elements)
        self.assertEqual(result.get_cardinality(), 3)
        self.assertTrue(1 in result)
        self.assertTrue(2 in result)
        self.assertTrue(3 in result)

class TestSetAdvanced(unittest.TestCase):

    def test_nested_sets(self):
        inner_set = Set()
        element = create_unique_set()
        inner_set.add_element(element)
        outer_set = Set()
        outer_set.add_element(inner_set)
        self.assertEqual(outer_set.get_cardinality(), 1)
        self.assertTrue(inner_set in outer_set)

    def test_complex_operations(self):
        set1 = Set()
        set2 = Set()
        set3 = Set()
        elem1, elem2, elem3 = create_unique_set(), create_unique_set(), create_unique_set()
        set1.add_element(elem1)
        set1.add_element(elem2)
        set2.add_element(elem2)
        set2.add_element(elem3)
        set3.add_element(elem1)
        result = (set1 + set2) * set3
        self.assertEqual(result.get_cardinality(), 1)
        self.assertTrue(elem1 in result)

    def test_power_set_properties(self):
        test_set = Set()
        elem1, elem2 = create_unique_set(), create_unique_set()
        test_set.add_element(elem1)
        test_set.add_element(elem2)
        power_set = test_set.get_power_set()
        empty_set_exists = False
        for subset in power_set:
            if subset.is_empty():
                empty_set_exists = True
                break
        self.assertTrue(empty_set_exists)
        original_set_exists = False
        for subset in power_set:
            if subset == test_set:
                original_set_exists = True
                break
        self.assertTrue(original_set_exists)

    def test_set_identity(self):
        set1 = Set([create_unique_set(), create_unique_set()])
        empty_set = Set()
        union_with_empty = set1 + empty_set
        self.assertEqual(union_with_empty, set1)
        intersection_with_empty = set1 * empty_set
        self.assertEqual(intersection_with_empty, empty_set)
        difference_with_empty = set1 - empty_set
        self.assertEqual(difference_with_empty, set1)

    def test_large_set_operations(self):
        set1 = Set()
        elements1 = [create_unique_set() for _ in range(3)]
        for elem in elements1:
            set1.add_element(elem)
        set2 = Set()
        elements2 = [create_unique_set() for _ in range(2)]
        for elem in elements2:
            set2.add_element(elem)
        union_set = set1 + set2
        self.assertEqual(union_set.get_cardinality(), 5)

class TestSetEdgeCases(unittest.TestCase):

    def test_self_operations(self):
        test_set = Set([create_unique_set(), create_unique_set()])
        union_with_self = test_set + test_set
        self.assertEqual(union_with_self, test_set)
        intersection_with_self = test_set * test_set
        self.assertEqual(intersection_with_self, test_set)
        difference_with_self = test_set - test_set
        self.assertTrue(difference_with_self.is_empty())

    def test_multiple_nesting(self):
        level1 = Set()
        level2 = Set()
        level3 = Set()
        element = create_unique_set()
        level3.add_element(element)
        level2.add_element(level3)
        level1.add_element(level2)
        self.assertEqual(level1.get_cardinality(), 1)
        self.assertEqual(level2.get_cardinality(), 1)
        self.assertEqual(level3.get_cardinality(), 1)

    def test_power_set_of_power_set(self):
        original_set = Set([create_unique_set(), create_unique_set()])
        power_set = original_set.get_power_set()
        power_set_of_power_set = power_set.get_power_set()
        self.assertEqual(power_set_of_power_set.get_cardinality(), 16)

    def test_remove_nonexistent_element(self):
        test_set = Set([create_unique_set(), create_unique_set()])
        original_cardinality = test_set.get_cardinality()
        nonexistent_element = create_unique_set()
        test_set.remove_element(nonexistent_element)
        self.assertEqual(test_set.get_cardinality(), original_cardinality)

    def test_empty_set_operations(self):
        empty1 = Set()
        empty2 = Set()
        non_empty = Set([create_unique_set()])
        self.assertEqual(empty1 + empty2, empty1)
        self.assertEqual(empty1 * non_empty, empty1)
        self.assertEqual(non_empty - empty1, non_empty)

if __name__ == '__main__':
    unittest.main(verbosity=2)