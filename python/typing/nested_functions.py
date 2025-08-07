from typing import assert_type

I, F = 2, 2.5


def xxx() -> None:
    def test_randint() -> None:
        def f1() -> float:
            g = I * F
            assert_type(g, int)
            return g

        assert_type(f1(), int)
