import unittest

from short_imports import shorten_imports


class ShortImportsTest(unittest.TestCase):
    def test_rewrites_multiline_import_and_its_references(self) -> None:
        source = """from ..one.two import (
    a,
    b as renamed,
    # More imports
)

result = a(renamed)
"""
        expected = """# More imports
from ..one import two

result = two.a(two.b)
"""
        self.assertEqual(shorten_imports(source), expected)

    def test_leaves_other_imports_and_shadowed_names_alone(self) -> None:
        source = """from one.two import (a, b)
from one.two import a
from one.two import (
    c,
)

def use(c):
    return c

result = c
"""
        expected = """from one.two import (a, b)
from one.two import a
from one import two

def use(c):
    return c

result = two.c
"""
        self.assertEqual(shorten_imports(source), expected)

    def test_skips_import_when_new_module_name_conflicts(self) -> None:
        source = """two = object()
from one.two import (
    a,
)
result = a
"""
        self.assertEqual(shorten_imports(source), source)

    def test_skips_import_when_module_name_is_shadowed_at_reference(self) -> None:
        source = """from one.two import (
    a,
)

def use(two):
    return a
"""
        self.assertEqual(shorten_imports(source), source)

    def test_skips_imports_that_would_bind_the_same_module_name(self) -> None:
        source = """from one.two import (
    a,
)
from other.two import (
    b,
)
result = a(b)
"""
        self.assertEqual(shorten_imports(source), source)

    def test_skips_same_module_name_across_nested_scopes(self) -> None:
        source = """from one.two import (
    a,
)

def use():
    from other.two import (
        b,
    )
    return a(b)
"""
        self.assertEqual(shorten_imports(source), source)


if __name__ == '__main__':
    unittest.main()
