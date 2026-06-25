from playwright.sync_api import Page, Locator
from base_page import BasePage


class ProductPage(BasePage):
    """
    Page object representing the product details page.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.product_name: Locator = page.locator(".product-detail__info h2")
        self.quantity_input: Locator = page.locator("#quantity")
        self.add_to_cart_button: Locator = page.locator(
            ".add-to-cart-form button[type='submit']"
        )
        self.add_to_wishlist_button: Locator = page.locator(
            ".add-to-wishlist-form button[type='submit']"
        )
        self.write_review_button: Locator = page.locator("a:has-text('Write a Review')")
        self.alerts: Locator = page.locator(".alert")

    def get_product_name(self) -> str:
        """
        Return the product name.
        """
        return self.product_name.inner_text().strip()

    def set_quantity(self, qty: int) -> None:
        """
        Fill the quantity field with the specified value.
        """
        self.quantity_input.fill(str(qty))

    def add_to_cart(self, qty: int = 1) -> None:
        """
        Specify a quantity and add the product to the cart.
        """
        self.set_quantity(qty)
        self.add_to_cart_button.click()

    def add_to_wishlist(self) -> None:
        """
        Add the product to the wishlist (only works if authenticated).
        """
        self.add_to_wishlist_button.click()

    def click_write_review(self) -> None:
        """
        Navigate to the write review page.
        """
        self.write_review_button.click()

    def get_alert_messages(self) -> list[str]:
        """
        Return text from all currently visible alert banner messages.
        """
        return self.alerts.all_inner_texts()
