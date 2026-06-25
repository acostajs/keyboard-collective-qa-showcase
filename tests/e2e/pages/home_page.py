from playwright.sync_api import Page, Locator
from base_page import BasePage


class HomePage(BasePage):
    """
    Page object representing the shop index/homepage.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.category_cards: Locator = page.locator(".category-card")
        self.product_cards: Locator = page.locator(".product-card")
        self.sort_select: Locator = page.locator("#id_sort")
        self.filter_apply_button: Locator = page.locator(
            ".filter-card button[type='submit']"
        )

    def navigate(self, base_url: str) -> None:
        """
        Navigate to the homepage using the base URL.
        """
        self.navigate_to(f"{base_url}/en/")

    def click_category_by_name(self, name: str) -> None:
        """
        Click on a category card matching the given name.
        """
        self.category_cards.filter(has_text=name).first.click()

    def click_product_by_name(self, name: str) -> None:
        """
        Click on a product card matching the given name.
        """
        self.product_cards.filter(has_text=name).first.click()

    def get_product_names(self) -> list[str]:
        """
        Return the names of all products currently displayed on the page.
        """
        return self.product_cards.locator(".product-card__title").all_inner_texts()

    def sort_by(self, criterion: str) -> None:
        """
        Select a sorting option and apply it.
        """
        self.sort_select.select_option(value=criterion)
        self.filter_apply_button.click()

    def check_filter_checkbox_by_label(self, label_text: str) -> None:
        """
        Check a filter checkbox based on its label text.
        """
        self.page.locator(f"label:has-text('{label_text}')").click()

    def apply_filters(self) -> None:
        """
        Submit the filter and sort form.
        """
        self.filter_apply_button.click()
