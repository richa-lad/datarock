import pytest
from pydantic import ValidationError
from src.exceptions import ItemNotInCatalogue
from src.checkout import Checkout
from src.models import PricingRule, Item
from src.pricing_rules import count_matching_items
from typing import Dict, List


# test 1 - check scan adds item
def test_scan_adds_item(pricing_rules: PricingRule, catalogue: Dict[str, Item]):
    co = Checkout(pricing_rules=pricing_rules, catalogue=catalogue)

    assert len(co.scanned_items) == 0

    co.scan(item_sku="atv")

    assert len(co.scanned_items) == 1


# test 2 - check scan raises error if item doesn't exist
def test_scan_raises_item_not_in_catalogue(
    pricing_rules: PricingRule, catalogue: Dict[str, Item]
):
    co = Checkout(pricing_rules=pricing_rules, catalogue=catalogue)

    with pytest.raises(ItemNotInCatalogue, match=r".*not found in catalogue.*"):
        co.scan("abc")


# test 3 - check scan raises error if item has wrong attributes
def test_scan_raises_error_bad_attribute(
    pricing_rules: PricingRule, catalogue: Dict[str, Item]
):
    co = Checkout(pricing_rules=pricing_rules, catalogue=catalogue)

    with pytest.raises(ValidationError):
        co.scan("bad-item")


# test 4 - check total calculates price
def test_correct_price():
    co = Checkout(pricing_rules=[], catalogue={})

    co.scanned_items = [
        Item(sku="", name="", price=10.00, currency=""),
        Item(sku="", name="", price=15.00, currency=""),
    ]

    assert co.total() == 25.00


# test 5 - check receipt returns items
def test_receipt():
    co = Checkout(pricing_rules=[], catalogue={})

    co.items_with_deals = [
        Item(sku="", name="", price=10.00, currency=""),
        Item(sku="", name="", price=15.00, currency=""),
    ]

    assert co.receipt() == co.items_with_deals


# test 6 - check count counts correctly
def test_count_matching_items(mock_items: List[Item]):
    count = count_matching_items(items=mock_items, sku_to_match="")

    assert count == 2

    count = count_matching_items(items=mock_items, sku_to_match="abc")

    assert count == 0
