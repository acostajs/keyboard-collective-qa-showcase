from playwright.sync_api import Page, Locator
from base_page import BasePage


class LoginPage(BasePage):
    """
    Page object representing the Login page.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input: Locator = page.locator("#id_username")
        self.password_input: Locator = page.locator("#id_password")
        self.login_button: Locator = page.locator(".login-btn")
        self.errors: Locator = page.locator(".alert-danger")

    def login(self, username: str, password: str) -> None:
        """
        Fill the login credentials and submit.
        """
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_messages(self) -> list[str]:
        """
        Return all displayed login error messages.
        """
        return self.errors.all_inner_texts()
