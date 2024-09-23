import logging
from typing import List

from src.models import Item

logger = logging.getLogger(__name__)


def count_matching_items(items: List[Item], sku_to_match: str):
    """Counts the number of items in the list that match the provided sku

    Args:
        items (List[Item]): Items to check
        sku_to_match (str): Sku to check for

    Returns:
        int: number of matching items
    """
    matching_items = [i for i in items if i.sku == sku_to_match]
    n_matching_items = len(matching_items)

    return n_matching_items


class NForMDeal:
    """Logic to apply the N for M deal e.g. 3 for 2."""

    def __init__(
        self,
        *,
        name: str,
        sku: str,
        purchase_number_required: str,
        number_to_pay_for: int
    ) -> None:
        self.name = name
        self.sku = sku
        self.purchase_number_required = purchase_number_required
        self.number_to_pay_for = number_to_pay_for

    def apply(self, items: List[Item]) -> List[Item]:
        """Applies the logic for the N for M Deal

        Args:
            items (List[Item]): All scanned items

        Returns:
            List[Item]: All scanned items with prices updated for any items where this deal applies.
        """
        # return a list of items with the price updated to 0 if the rule applies
        n_free_items = 0
        self.n_matching_items = count_matching_items(items=items, sku_to_match=self.sku)
        if self.n_matching_items >= self.purchase_number_required:
            logger.info("Qualifies for NForMDeal")
            n_free_items = self.purchase_number_required // self.number_to_pay_for

            for ix, item in enumerate(items):
                if item.sku == self.sku:
                    items[ix] = items[ix].update(attr_to_update="price", new_value=0.0)

                    n_free_items -= 1
                if n_free_items <= 0:
                    break

        return items


class BulkDiscountDeal:
    """Logic for the Bulk Discount Deal e.g. buy more than 4 of an item and have the price reduced for all of these items."""

    def __init__(
        self,
        *,
        name: str,
        sku: str,
        purchase_number_required: str,
        new_item_price: float
    ) -> None:
        self.name = name
        self.sku = sku
        self.purchase_number_required = purchase_number_required
        self.new_item_price = new_item_price

    def apply(self, items: List[Item]) -> List[Item]:
        """Applies the logic for the Bulk Discount deal.

        Args:
            items (List[Item]): All scanned items

        Returns:
            List[Item]: All scanned items with prices updated for any items where this deal applies.
        """
        # return a list of items with the price updated to 0 if the rule applies
        n_repriced_items = 0
        self.n_matching_items = count_matching_items(items=items, sku_to_match=self.sku)
        if self.n_matching_items > self.purchase_number_required:
            logger.info("Qualifies for Bulk Discount Deal")
            n_repriced_items = self.n_matching_items

            for ix, item in enumerate(items):
                if item.sku == self.sku:
                    items[ix] = items[ix].update(
                        attr_to_update="price", new_value=self.new_item_price
                    )

                    n_repriced_items -= 1
                if n_repriced_items <= 0:
                    break

        return items


class FreeItemDeal:
    """Logic for the Free Item Deal e.g. buy an item and receive a free item with it."""

    def __init__(
        self,
        *,
        name: str,
        sku: str,
        purchase_number_required: str,
        item_sku: str,
        n_free_items: int
    ) -> None:
        self.name = name
        self.sku = sku
        self.purchase_number_required = purchase_number_required
        self.item_sku = item_sku
        self.n_free_items = n_free_items

    def apply(self, items: List[Item]) -> List[Item]:
        """Applies the logic for the Free Item Deal.

        Args:
            items (List[Item]): All scanned items

        Returns:
            List[Item]: All scanned items with prices updated for any items where this deal applies.
        """
        # add the free item(s) with price = 0
        self.n_matching_items = count_matching_items(items=items, sku_to_match=self.sku)
        if self.n_matching_items >= self.purchase_number_required:
            logger.info("Qualifies for Free Item Deal")
            # if item sku is already in items, make it free
            # the deal says we get n_free_items for every purchase_number_required
            number_for_free = (
                self.n_matching_items // self.purchase_number_required
            ) * self.n_free_items
            # if there are any of the free items already in the list of items, make these free first
            for ix, item in enumerate(items):
                if item.sku == self.item_sku:
                    items[ix] = items[ix].update(attr_to_update="price", new_value=0.0)
                    number_for_free -= 1
                if number_for_free <= 0:
                    break

            # if number_for_free still more than 0, add a free one
            while number_for_free > 0:
                items.append(
                    Item(
                        sku=self.item_sku, name="FreeItem", price=0.0, currency="dollar"
                    )
                )
                number_for_free -= 1

        return items
