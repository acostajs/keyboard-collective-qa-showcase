import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.account_page import AccountPage


@pytest.mark.django_db
def test_user_auth_journey(page: Page, live_server, fake_user) -> None:
    """
    Verify the complete end-to-end user journey for authentication:
    1. Navigate to the Homepage
    2. Click Register in navigation header
    3. Register a new user using fake_user data
    4. Log in with the newly registered user credentials
    5. Verify redirection to account dashboard and correct username display
    6. Log out and verify redirection back to login
    """
    home = HomePage(page)
    reg_page = RegistrationPage(page)
    login_page = LoginPage(page)
    account_page = AccountPage(page)

    # 1. Navigate to Homepage
    home.navigate(live_server.url)

    # 2. Click "Register" link in top nav
    home.register_link.click()
    assert "/account/registration/" in page.url

    # 3. Register a new user
    reg_page.register(fake_user)

    # 4. Verify redirected to login page after successful registration
    assert "/account/login/" in page.url

    # 5. Log in with registered credentials
    login_page.login(fake_user["username"], fake_user["password1"])

    # 6. Verify redirected to account dashboard
    assert page.url.endswith("/account/")

    # 7. Verify account dashboard displays correct username
    assert account_page.get_username() == fake_user["username"]

    # 8. Log out
    account_page.logout()

    # Verify redirected back to login page
    assert "/account/login/" in page.url
