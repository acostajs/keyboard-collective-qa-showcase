from playwright.sync_api import Page, Locator
from base_page import BasePage


class RegistrationPage(BasePage):
    """
    Page object representing the User Registration page.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.username_input: Locator = page.locator("#id_username")
        self.first_name_input: Locator = page.locator("#id_first_name")
        self.last_name_input: Locator = page.locator("#id_last_name")
        self.email_input: Locator = page.locator("#id_email")
        self.password1_input: Locator = page.locator("#id_password1")
        self.password2_input: Locator = page.locator("#id_password2")
        self.address_line1_input: Locator = page.locator("#id_address_line1")
        self.address_line2_input: Locator = page.locator("#id_address_line2")
        self.city_input: Locator = page.locator("#id_city")
        self.postal_code_input: Locator = page.locator("#id_postal_code")
        self.country_input: Locator = page.locator("#id_country")
        self.register_button: Locator = page.locator(".registration-btn")
        self.field_errors: Locator = page.locator(".text-danger")

    def register(self, data: dict[str, str]) -> None:
        """
        Fill in the registration form and submit.
        The data dictionary should map field keys to values.
        """
        if "username" in data:
            self.username_input.fill(data["username"])
        if "first_name" in data:
            self.first_name_input.fill(data["first_name"])
        if "last_name" in data:
            self.last_name_input.fill(data["last_name"])
        if "email" in data:
            self.email_input.fill(data["email"])
        if "password1" in data:
            self.password1_input.fill(data["password1"])
        if "password2" in data:
            self.password2_input.fill(data["password2"])
        if "address_line1" in data:
            self.address_line1_input.fill(data["address_line1"])
        if "address_line2" in data:
            self.address_line2_input.fill(data["address_line2"])
        if "city" in data:
            self.city_input.fill(data["city"])
        if "postal_code" in data:
            self.postal_code_input.fill(data["postal_code"])
        if "country" in data:
            self.country_input.fill(data["country"])
        self.register_button.click()

    def get_error_messages(self) -> list[str]:
        """
        Return any visible validation error messages on the form.
        """
        return self.field_errors.all_inner_texts()
