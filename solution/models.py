from typing import List, Protocol
from pydantic import BaseModel

class Item(BaseModel):
    sku: str
    name: str
    price: float
    currency: str

class PricingRule(Protocol):

    def __init__(self, *args, **kwargs) -> None:
        ...

    def qualifies(self, items: List[Item]) -> bool:
        ...

    def apply(self, items: List[Item]) -> List[Item]:
        ...