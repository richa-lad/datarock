from typing import List, Dict
from src.exceptions import ItemNotInCatalogue
from src.models import PricingRule, Item
import logging

logger = logging.getLogger(__name__)


class Checkout:

    def __init__(self, pricing_rules: List[PricingRule], catalogue: Dict[str, Item]):
        """Creates Checkout object.

        Args:
            pricing_rules (List[PricingRule]): A list of rules that specify logic relating to offers.
            catalogue (Dict[str, Item]): All items available, indexed by their unique sku.
        """
        self.pricing_rules = pricing_rules
        self.scanned_items = list()
        self.catalogue = catalogue

    def scan(self, item_sku: str) -> None:
        """Adds an item to the list of items being purchased

        Args:
            item_sku (str): Unique identifier of the item.
        """
        item_attrs = self.catalogue.get(item_sku)
        if item_attrs is None:
            raise ItemNotInCatalogue(f"Item with sku {item_sku} not found in catalogue.")
        item = Item(**item_attrs)
        self.scanned_items.append(item)

    def total(self) -> float:
        """Calculates the total sum of all scanned items, with any discounts applied.

        Returns:
            float: The total cost of the scanned items.
        """
        self.items_with_deals = self.scanned_items.copy()
        for rule in self.pricing_rules:
            self.items_with_deals = rule.apply(self.items_with_deals)
        return sum(item.price for item in self.items_with_deals)

    def receipt(self) -> List[Item]:
        """Returns the list of all scanned items, with any discounts applied.

        Returns:
            List[Item]: _description_
        """
        return self.items_with_deals
