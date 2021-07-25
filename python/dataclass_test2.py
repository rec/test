from dataclasses import dataclass

@dataclass
class Modifier:
    value: str
    name: str
    hidden: str
    generate_add_modifiers: str


@dataclass
class Derived(Modifier):
    is_position: bool
