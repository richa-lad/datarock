import yaml
from pricing_rules import (
    BulkDiscountDeal,
    NForMDeal,
    FreeItemDeal
)

from checkout import Checkout

if __name__ == "__main__":
    # load pricing rules
    with open("specials.yaml") as f:
        deals = yaml.safe_load(f)
    
    free_item_deals = deals["FreeItemDeals"]
    bulk_discount_deals = deals["BulkDiscountDeals"]
    n_for_m_deals = deals["NForMDeals"]

    pricing_rules = list()

    for deal in free_item_deals:
        pricing_rules.append(
            FreeItemDeal(
                **deal
            )
        )

    for deal in bulk_discount_deals:
        pricing_rules.append(
            BulkDiscountDeal(
                **deal
            )
        )

    for deal in n_for_m_deals:
        pricing_rules.append(
            NForMDeal(
                **deal
            )
        )

    # construct checkout object
    with open("catalogue.yaml") as f:
        catalogue = yaml.safe_load(f)

    co = Checkout(
        pricing_rules=pricing_rules,
        catalogue=catalogue
    )

    # scan things
    items_to_scan = ["atv", "ipd", "ipd", "atv", "ipd", "ipd", "ipd"]
    for sku in items_to_scan:
        co.scan(sku)
    print(co.total())