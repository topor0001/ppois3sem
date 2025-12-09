class Rectangle:
    DEFAULT_COORDINATE = 0
    DEFAULT_DIMENSION = 1

    def __init__(self, x=None, y=None, width=None, height=None):
        if x is None or y is None or width is None or height is None:
            self._x = self.DEFAULT_COORDINATE
            self._y = self.DEFAULT_COORDINATE
            self._width = self.DEFAULT_DIMENSION
            self._height = self.DEFAULT_DIMENSION
        else:
            self._x = x
            self._y = y
            self._width = width
            self._height = height
        self._normalize()

    def _normalize(self):
        if self._width < 0:
            self._x += self._width
            self._width = -self._width
        if self._height < 0:
            self._y += self._height
            self._height = -self._height

    def _min(self, a, b):
        return a if a < b else b

    def _max(self, a, b):
        return a if a > b else b

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_vertices(self):
        return [
            (self._x, self._y),
            (self._x + self._width, self._y),
            (self._x + self._width, self._y + self._height),
            (self._x, self._y + self._height)
        ]

    def move(self, delta_x, delta_y):
        self._x += delta_x
        self._y += delta_y

    def resize(self, new_width, new_height):
        self._width = new_width
        self._height = new_height
        self._normalize()

    def __pos__(self):
        return Rectangle(self._x, self._y, self._width + 1, self._height + 1)

    def __neg__(self):
        new_width = self._width - 1 if self._width > 1 else 1
        new_height = self._height - 1 if self._height > 1 else 1
        return Rectangle(self._x, self._y, new_width, new_height)

    def __add__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented

        min_x = self._min(self._x, other._x)
        min_y = self._min(self._y, other._y)
        max_x = self._max(self._x + self._width, other._x + other._width)
        max_y = self._max(self._y + self._height, other._y + other._height)

        return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

    def __iadd__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented

        result = self + other
        self._x, self._y, self._width, self._height = (
            result._x, result._y, result._width, result._height
        )
        return self

    def __sub__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented

        left = self._max(self._x, other._x)
        bottom = self._max(self._y, other._y)
        right = self._min(self._x + self._width, other._x + other._width)
        top = self._min(self._y + self._height, other._y + other._height)

        if right <= left or top <= bottom:
            return Rectangle()

        return Rectangle(left, bottom, right - left, top - bottom)

    def __isub__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented

        result = self - other
        self._x, self._y, self._width, self._height = (
            result._x, result._y, result._width, result._height
        )
        return self

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (self._x == other._x and self._y == other._y and
                self._width == other._width and self._height == other._height)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return f"Rectangle(x={self._x}, y={self._y}, width={self._width}, height={self._height})"

    def __repr__(self):
        return f"Rectangle({self._x}, {self._y}, {self._width}, {self._height})"

    def from_string(self, string_repr):
        """Creating a rectangle from a string"""
        try:

            parts = []
            current = ""
            for char in string_repr:
                if char == ' ':
                    if current:
                        parts.append(current)
                    current = ""
                else:
                    current += char
            if current:
                parts.append(current)

            if len(parts) != 4:
                raise ValueError("String must contain exactly 4 numbers")


            def str_to_int(s):
                result = 0
                sign = 1
                start = 0

                if s and s[0] == '-':
                    sign = -1
                    start = 1
                elif s and s[0] == '+':
                    start = 1

                for i in range(start, len(s)):
                    digit = ord(s[i]) - ord('0')
                    if 0 <= digit <= 9:
                        result = result * 10 + digit
                    else:
                        raise ValueError(f"Invalid number: {s}")

                return result * sign

            x = str_to_int(parts[0])
            y = str_to_int(parts[1])
            width = str_to_int(parts[2])
            height = str_to_int(parts[3])

            return self.__class__(x, y, width, height)
        except Exception as e:
            raise ValueError(f"Invalid rectangle string: {string_repr}") from e

    def create_from_string(self, string_repr):
        """Creating a new rectangle from a string"""
        return self.from_string(string_repr)

    def to_string(self):
        """Converting a rectangle to a string"""
        def int_to_str(n):
            if n == 0:
                return "0"

            result = ""
            negative = n < 0
            n = abs(n)

            while n > 0:
                digit = n % 10
                result = chr(ord('0') + digit) + result
                n = n // 10

            return "-" + result if negative else result

        return f"{int_to_str(self._x)} {int_to_str(self._y)} {int_to_str(self._width)} {int_to_str(self._height)}"

    def copy(self):
        return Rectangle(self._x, self._y, self._width, self._height)

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy()

def rectangle_from_string(string_repr):
    """Creating a rectangle from a string (external function)"""
    return Rectangle().from_string(string_repr)


def create_rectangle_default():
    """Create a rectangle with default settings"""
    return Rectangle()