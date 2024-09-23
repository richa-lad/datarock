from typing import Any, List, Protocol
from pydantic import BaseModel


class Item(BaseModel):
    sku: str
    name: str
    price: float
    currency: str

    def update(self, attr_to_update: str, new_value: Any):
        """Returns a new version of the item with the relevant field updated.

        Args:
            attr_to_update (str): The field to update
            new_value (Any): The updated value of the field.

        Returns:
            Item: A new version of the Item.
        """
        current = self.model_dump()
        current[attr_to_update] = new_value

        new = Item(**current)

        return new


class PricingRule(Protocol):

    def __init__(self, *args, **kwargs) -> None: ...

    def apply(self, items: List[Item]) -> List[Item]: ...
