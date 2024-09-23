from typing import List, Dict
from models import PricingRule, Item
import logging

logger = logging.getLogger(__name__)


class Checkout:

    def __init__(self, pricing_rules: List[PricingRule], catalogue: Dict[str, Item]):
        self.pricing_rules = pricing_rules
        self.scanned_items = list()
        self.catalogue = catalogue

    def scan(self, item_sku: str) -> None:
        item_attrs = self.catalogue.get(item_sku)
        item = Item(**item_attrs)
        self.scanned_items.append(item)

    def total(self):
        self.items_with_deals = self.scanned_items.copy()
        for rule in self.pricing_rules:
            self.items_with_deals = rule.apply(self.items_with_deals)
        return sum(item.price for item in self.items_with_deals)

    def receipt(self):
        return self.items_with_deals
