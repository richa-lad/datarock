import json
import logging

import yaml

from src.pricing_rules import BulkDiscountDeal, NForMDeal, FreeItemDeal
from src.checkout import Checkout

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # load pricing rules
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

    # construct checkout object
    with open("data/catalogue.yaml") as f:
        catalogue = yaml.safe_load(f)

    co = Checkout(pricing_rules=pricing_rules, catalogue=catalogue)

    # scan things
    items_to_scan = input(
        "Enter the skus of the items you would like to be scanned, separated by a comma: "
    )
    items_to_scan = items_to_scan.replace(" ", "")
    items_to_scan = items_to_scan.split(",")
    for sku in items_to_scan:
        co.scan(sku)
    print(f"Total: ${co.total()}")

    view_receipt = input(
        "Do you want to see an itemized receipt with discounts applied? (y/n) "
    )
    if view_receipt.lower() == "y":
        print(json.dumps([i.model_dump() for i in co.receipt()], indent=2))
