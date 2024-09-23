from typing import Any, List, Protocol
from pydantic import BaseModel


class Item(BaseModel):
    sku: str
    name: str
    price: float
    currency: str

    def update(self, attr_to_update: str, new_value: Any):
        current = self.model_dump()
        current[attr_to_update] = new_value

        new = Item(**current)

        return new


class PricingRule(Protocol):

    def __init__(self, *args, **kwargs) -> None: ...

    def qualifies(self, items: List[Item]) -> bool: ...

    def apply(self, items: List[Item]) -> List[Item]: ...
