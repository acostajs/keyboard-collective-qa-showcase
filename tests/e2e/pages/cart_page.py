from playwright.sync_api import Page, Locator
from base_page import BasePage


class CartPage(BasePage):
    """
    Page object representing the shopping cart detail page.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_table: Locator = page.locator(".cart-table")
        self.clear_cart_button: Locator = page.locator("button:has-text('Clear Cart')")
        self.checkout_link: Locator = page.locator("a:has-text('Checkout')")
        self.empty_cart_message: Locator = page.locator(
            "p:has-text('Your cart is empty.')"
        )
        self.continue_shopping_link: Locator = page.locator(
            "a:has-text('Continue Shopping')"
        )

    def get_cart_item_rows(self) -> Locator:
        """
        Return the Locator for the rows of items in the cart table.
        """
        return self.cart_table.locator("tbody tr")

    def get_cart_item_count(self) -> int:
        """
        Return the number of unique items currently in the cart.
        """
        if not self.cart_table.is_visible():
            return 0
        return self.get_cart_item_rows().count()

    def get_cart_item_by_name(self, product_name: str) -> Locator:
        """
        Find and return the table row locator for a product name.
        """
        return self.get_cart_item_rows().filter(has_text=product_name).first

    def update_item_quantity(self, product_name: str, qty: int) -> None:
        """
        Update the quantity of a product in the cart.
        """
        row = self.get_cart_item_by_name(product_name)
        quantity_input = row.locator("input[name='quantity']")
        quantity_input.fill(str(qty))
        row.locator("button:has-text('Update')").click()

    def remove_item(self, product_name: str) -> None:
        """
        Remove a product from the cart.
        """
        row = self.get_cart_item_by_name(product_name)
        row.locator("button:has-text('Remove')").click()

    def clear_cart(self) -> None:
        """
        Clear all items from the cart.
        """
        self.clear_cart_button.click()

    def proceed_to_checkout(self) -> None:
        """
        Click the checkout button.
        """
        self.checkout_link.click()

    def get_subtotal(self) -> str:
        """
        Return the cart subtotal text (e.g. '$120.00').
        """
        return self.cart_table.locator("tfoot tr td").nth(1).inner_text().strip()
