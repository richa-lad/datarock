import pytest
import yaml
from src.pricing_rules import FreeItemDeal, BulkDiscountDeal, NForMDeal
from src.models import Item


@pytest.fixture
def mock_items():
    items = [
        Item(sku="", name="", price=10.00, currency=""),
        Item(sku="", name="", price=15.00, currency=""),
    ]

    return items


@pytest.fixture
def pricing_rules():
    with open("data/specials.yaml") as f:
        deals = yaml.safe_load(f)

    free_item_deals = deals["FreeItemDeals"]
    bulk_discount_deals = deals["BulkDiscountDeals"]
    n_for_m_deals = deals["NForMDeals"]

    pricing_rules = list()

    for deal in free_item_deals:
        pricing_rules.append(FreeItemDeal(**deal))

    for deal in bulk_discount_deals:
        pricing_rules.append(BulkDiscountDeal(**deal))

    for deal in n_for_m_deals:
        pricing_rules.append(NForMDeal(**deal))

    return pricing_rules


@pytest.fixture
def catalogue():
    with open("data/catalogue.yaml") as f:
        catalogue = yaml.safe_load(f)
    return catalogue
