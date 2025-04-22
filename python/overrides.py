from typing_extensions import override


class Base:
    def method(self) -> None:
        """Base"""
        pass


class Derived1(Base):
    def method(self) -> None:
        pass


class Derived2(Base):
    def method(self) -> None:
        """Derived2"""
        pass


class Derived3(Base):
    @override
    def method(self) -> None:
        pass


class Derived4(Base):
    @override
    def method(self) -> None:
        """Derived4"""
        pass


help(Base.method)      # prints Base
help(Derived1.method)  # prints Base
help(Derived2.method)  # prints Derived2
help(Derived3.method)  # prints Base
help(Derived4.method)  # prints Derived4
