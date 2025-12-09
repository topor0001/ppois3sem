class Set:
    MAX_NESTING_LEVEL = 100
    _set_counter = 0

    def __init__(self, elements=None, unique_id=None):
        Set._set_counter += 1
        self._elements = []
        self._id = unique_id or Set._set_counter
        if elements is not None:
            for element in elements:
                self.add_element(element)

    def _contains_element(self, element):
        for elem in self._elements:
            if self._elements_equal(elem, element):
                return True
        return False

    def _elements_equal(self, elem1, elem2):
        if isinstance(elem1, Set) and isinstance(elem2, Set):
            return elem1._id == elem2._id
        else:
            return elem1 == elem2

    def is_empty(self):
        return len(self._elements) == 0

    def add_element(self, element):
        if not self._contains_element(element):
            self._elements.append(element)

    def remove_element(self, element):
        new_elements = []
        for elem in self._elements:
            if not self._elements_equal(elem, element):
                new_elements.append(elem)
        self._elements = new_elements

    def get_cardinality(self):
        return len(self._elements)

    def __contains__(self, element):
        return self._contains_element(element)

    def __getitem__(self, element):
        return self._contains_element(element)

    def __add__(self, other):
        if not isinstance(other, Set):
            return NotImplemented

        result = Set()
        for elem in self._elements:
            result.add_element(elem)
        for elem in other._elements:
            result.add_element(elem)
        return result

    def __iadd__(self, other):
        if not isinstance(other, Set):
            return NotImplemented
        for elem in other._elements:
            self.add_element(elem)
        return self

    def __mul__(self, other):
        if not isinstance(other, Set):
            return NotImplemented
        result = Set()
        for elem in self._elements:
            if elem in other:
                result.add_element(elem)
        return result

    def __imul__(self, other):
        if not isinstance(other, Set):
            return NotImplemented
        new_elements = []
        for elem in self._elements:
            if elem in other:
                new_elements.append(elem)
        self._elements = new_elements
        return self

    def __sub__(self, other):
        if not isinstance(other, Set):
            return NotImplemented
        result = Set()
        for elem in self._elements:
            if elem not in other:
                result.add_element(elem)
        return result

    def __isub__(self, other):
        if not isinstance(other, Set):
            return NotImplemented
        new_elements = []
        for elem in self._elements:
            if elem not in other:
                new_elements.append(elem)
        self._elements = new_elements
        return self

    def get_power_set(self):
        elements_list = self._elements
        n = len(elements_list)
        total_subsets = 1 << n
        all_subsets = []
        for i in range(total_subsets):
            subset = Set(unique_id=f"subset_{i}")
            for j in range(n):
                if i & (1 << j):
                    subset.add_element(elements_list[j])
            all_subsets.append(subset)
        power_set = Set(unique_id="power_set")
        for subset in all_subsets:
            power_set.add_element(subset)

        return power_set

    def __eq__(self, other):
        if not isinstance(other, Set):
            return NotImplemented
        if len(self._elements) != len(other._elements):
            return False
        for elem in self._elements:
            if not other._contains_element(elem):
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        if self.is_empty():
            return "{}"
        elements_str = []
        for elem in self._elements:
            if isinstance(elem, Set):
                elements_str.append(str(elem))
            else:
                elements_str.append(repr(elem))
        return "{" + ", ".join(elements_str) + "}"

    def __repr__(self):
        return f"Set(elements={len(self._elements)})"

    def __iter__(self):
        return _SetIterator(self._elements)

    def __len__(self):
        return len(self._elements)

    def from_string(self, string_repr):
        """Creating a set from a string"""
        return self._parse_from_string(string_repr.strip())

    def _parse_from_string(self, string_repr, level=0):
        """Parsing a string into a set"""
        if self._check_nesting_level(level):
            raise ValueError("Maximum nesting level exceeded")
        
        string_repr = string_repr.strip()
        if not self._validate_string_format(string_repr):
            raise ValueError("Set must be enclosed in curly braces")
        
        return self._parse_set_content(string_repr, level)

    def _check_nesting_level(self, level):
        """Checking the nesting level"""
        return level > Set.MAX_NESTING_LEVEL

    def _validate_string_format(self, string_repr):
        """Checking string format"""
        return string_repr.startswith('{') and string_repr.endswith('}')

    def _parse_set_content(self, string_repr, level):
        """Parsing the contents of a set"""
        content = string_repr[1:-1].strip()
        if not content:
            return Set()
        
        return self._process_content_elements(content, level)

    def _process_content_elements(self, content, level):
        """Processing content elements"""
        result = Set()
        brace_count = 0
        current_element = []
        
        for char in content:
            brace_count, current_element = self._process_char(
                char, brace_count, current_element, result, level
            )
        

        self._process_final_element(current_element, result, level)
        
        return result

    def _process_char(self, char, brace_count, current_element, result_set, level):
        """Processing a single character"""
        if char == '{':
            brace_count += 1
            current_element.append(char)
        elif char == '}':
            brace_count -= 1
            current_element.append(char)
        elif char == ',' and brace_count == 0:
            self._process_element(current_element, result_set, level)
            current_element = []
        else:
            current_element.append(char)
        
        return brace_count, current_element

    def _process_element(self, element_chars, result_set, level):
        """Processing a completed item"""
        element_str = self._chars_to_string(element_chars).strip()
        if element_str:
            element = self._create_element_from_string(element_str, level)
            result_set.add_element(element)

    def _process_final_element(self, element_chars, result_set, level):
        """Processing the last element"""
        element_str = self._chars_to_string(element_chars).strip()
        if element_str:
            element = self._create_element_from_string(element_str, level)
            result_set.add_element(element)

    def _create_element_from_string(self, element_str, level):
        """Creating an element from a string"""
        if element_str.startswith('{'):
            return self._parse_from_string(element_str, level + 1)
        else:

            simple_element = element_str.strip()
      
            try:
            
                if simple_element.isdigit() or (simple_element[0] == '-' and simple_element[1:].isdigit()):
                    return int(simple_element)
            
                if (len(simple_element) >= 2 and 
                    ((simple_element[0] == "'" and simple_element[-1] == "'") or
                     (simple_element[0] == '"' and simple_element[-1] == '"'))):
                    return simple_element[1:-1]
            except:
                pass
            return simple_element

    def _chars_to_string(self, chars):
        """Converting a list of characters to a string"""
        return ''.join(chars)

    def parse_string(self, string_repr):
        """Parsing a string as a regular instance method"""
        return self._parse_from_string(string_repr)

    def copy(self):
        new_set = Set()
        for element in self._elements:
            if isinstance(element, Set):
                copied_element = Set(unique_id=element._id)
                for sub_elem in element._elements:
                    copied_element.add_element(sub_elem)
                new_set.add_element(copied_element)
            else:
                new_set.add_element(element)
        return new_set

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy()

    def __del__(self):
        Set._set_counter -= 1

def set_from_string(string_repr):
    """Creating a set from a string (external function)"""
    return Set().from_string(string_repr)


def create_empty_set():
    """Creating an empty set"""
    return Set()


def create_set_from_elements(elements):
    """Creating a set from a list of elements"""
    return Set(elements)


class _SetIterator:
    def __init__(self, elements):
        self._elements = elements
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._elements):
            result = self._elements[self._index]
            self._index += 1
            return result
        raise StopIteration