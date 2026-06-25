import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.django_db
def test_guest_shopping_journey(page: Page, live_server, seed_data) -> None:
    """
    Verify the complete end-to-end user journey of a guest:
    1. Browse catalog on homepage
    2. Search for a product
    3. Click on a product to view details
    4. Add product to cart with custom quantity
    5. View cart and verify prices and quantity
    6. Update item quantity in cart and verify recalculations
    7. Clear the cart
    """
    # 1. Navigate to the Homepage
    home = HomePage(page)
    home.navigate(live_server.url)

    # Verify all products in the seeded DB are visible
    initial_products = home.get_product_names()
    assert "Keychron Q1" in initial_products
    assert "MX Master 3S" in initial_products
    assert "Cable Organizer" in initial_products

    # 2. Search for "MX Master"
    home.search_for("MX Master")

    # Verify search results page shows only the matched product
    searched_products = home.get_product_names()
    assert "MX Master 3S" in searched_products
    assert "Keychron Q1" not in searched_products

    # 3. View Product details page
    home.click_product_by_name("MX Master 3S")

    # Verify product page is loaded
    product_page = ProductPage(page)
    assert product_page.get_product_name() == "MX Master 3S"

    # 4. Add 2 units of the product to the cart
    product_page.add_to_cart(qty=2)

    # Verify redirection to the cart page
    assert "/cart/" in page.url
    cart_page = CartPage(page)

    # Verify cart item count, name, and total ($99.00 * 2 = $198.00)
    assert cart_page.get_cart_item_count() == 1
    assert cart_page.get_subtotal() == "$198.00"

    # 5. Update quantity to 3
    cart_page.update_item_quantity("MX Master 3S", qty=3)

    # Verify subtotal is updated ($99.00 * 3 = $297.00)
    assert cart_page.get_subtotal() == "$297.00"

    # 6. Clear the cart
    cart_page.clear_cart()

    # Verify cart is empty
    assert cart_page.empty_cart_message.is_visible()
    assert cart_page.get_cart_item_count() == 0
