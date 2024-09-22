from typing import List
from models import Item


class NForMDeal:

    def __init__(self, *, name: str, sku: str, purchase_number_required: str, number_to_pay_for: int) -> None:
        self.name = name
        self.sku = sku
        self.purchase_number_required = purchase_number_required
        self.number_to_pay_for = number_to_pay_for
    
    def qualifies(self, items: List[Item]) -> bool:
        self.matching_items = [i for i in items if i.sku == self.sku]
        self.n_matching_items = len(self.matching_items)

        return self.n_matching_items >= self.purchase_number_required

    def apply(self, items: List[Item]) -> List[Item]:
        # return a list of items with the price updated to 0 if the rule applies
        n_free_items = 0
        if self.qualifies(items=items):
            print("Qualifies for NForMDeal")
            n_free_items = self.purchase_number_required // self.number_to_pay_for
        
            k = 0
            for ix, item in enumerate(items):
                if item.sku == self.sku:
                    items[ix] = Item(
                        sku=item.sku,
                        name=item.name,
                        price=0.0,
                        currency=item.currency
                    )

                    k += 1
                if k == n_free_items:
                    break
                
        return items


class BulkDiscountDeal:

    def __init__(self, *, name: str, sku: str, purchase_number_required: str, new_item_price: float) -> None:
        self.name = name
        self.sku = sku
        self.purchase_number_required = purchase_number_required
        self.new_item_price = new_item_price

    def qualifies(self, items: List[Item]) -> bool:
        self.matching_items = [i for i in items if i.sku == self.sku]
        self.n_matching_items = len(self.matching_items)

        return self.n_matching_items > self.purchase_number_required

    def apply(self, items: List[Item]) -> List[Item]:
        # return a list of items with the price updated to 0 if the rule applies
        n_repriced_items = 0
        if self.qualifies(items=items):
            print("Qualifies for Bulk Discount Deal")
            n_repriced_items = self.n_matching_items
        
            k = 0
            for ix, item in enumerate(items):
                if item.sku == self.sku:
                    items[ix] = Item(
                        sku=item.sku,
                        name=item.name,
                        price=self.new_item_price,
                        currency=item.currency
                    )

                    k += 1
                if k == n_repriced_items:
                    break

        return items
    

class FreeItemDeal:

    def __init__(self, *, name: str, sku: str, purchase_number_required: str, item_sku: str, n_free_items: int) -> None:
        self.name = name
        self.sku = sku
        self.purchase_number_required = purchase_number_required
        self.item_sku = item_sku
        self.n_free_items = n_free_items

    def qualifies(self, items: List[Item]) -> bool:
        self.matching_items = [i for i in items if i.sku == self.sku]
        self.n_matching_items = len(self.matching_items)

        return self.n_matching_items >= self.purchase_number_required

    def apply(self, items: List[Item]) -> List[Item]:
        # add the free item(s) with price = 0
        if self.qualifies(items=items):
            print("Qualifies for Free Item Deal")
            # if item sku is already in items, make it free
            # the deal says we get n_free_items for every purchase_number_required
            number_for_free = (self.n_matching_items // self.purchase_number_required)*self.n_free_items
            # if there are any of the free items already in the list of items, make these free first
            for i, item in enumerate(items):
                if item.sku == self.item_sku:
                    items[i] = Item(
                        sku=item.sku,
                        name=item.name,
                        price=0.0,
                        currency=item.currency
                    )
                    number_for_free -= 1
                if number_for_free <= 0:
                    break

            # if number_for_free still more than 0, add a free one
            while number_for_free >= 0:
                items.append(Item(
                    sku=self.item_sku,
                    name="FreeItem",
                    price=0.0,
                    currency="dollar"
                ))
                number_for_free -= 1

        return items
