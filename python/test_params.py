import pytest
parametrize = pytest.mark.parametrize

from unittest import mock, TestCase




class MyTest(TestCase):
    @parametrize("a", (1, 2))
    def test_is_one(self, a):
        self.assertEqual(a, 1)
