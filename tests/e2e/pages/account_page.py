from playwright.sync_api import Page, Locator
from base_page import BasePage


class AccountPage(BasePage):
    """
    Page object representing the User Account Dashboard page.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_heading: Locator = page.locator(".account-username")
        self.logout_button: Locator = page.locator(".logout-btn")
        self.order_items: Locator = page.locator("ul.list-unstyled li")

    def get_username(self) -> str:
        """
        Return the username displayed on the dashboard.
        """
        return self.username_heading.inner_text().strip()

    def logout(self) -> None:
        """
        Log out the current user session by clicking the Logout button.
        """
        self.logout_button.click()

    def get_order_count(self) -> int:
        """
        Return the number of orders displayed on the dashboard.
        """
        if (
            self.order_items.count() == 1
            and "No orders yet" in self.order_items.first.inner_text()
        ):
            return 0
        return self.order_items.count()

    def click_view_order_by_id(self, order_id: int) -> None:
        """
        Click on the "View" button for the order matching the given ID.
        """
        self.order_items.filter(has_text=f"Order #{order_id}").locator(
            "a:has-text('View')"
        ).click()
