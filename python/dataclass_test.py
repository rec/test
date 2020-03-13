from dataclasses import dataclass


@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    "after name"

    unit_price: float
    "after price"
    quantity_on_hand: int = 0
    "after qtty"

    @property
    def total_cost(self) -> float:
        "inside tc!"
        return self.unit_price * self.quantity_on_hand
