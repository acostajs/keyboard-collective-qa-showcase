import pytest
from django.urls import reverse
from django.test import Client
from inventory.models import Category, Product


@pytest.mark.django_db
def test_guest_shopping_cart_flow(
    test_client: Client, seed_data: tuple[Category, Product, Product, Product]
) -> None:
    """
    Integration test for the guest shopping cart flow using TestClient.
    """
    category, p1, p2, p3 = seed_data

    # 1. Verify cart is initially empty
    response = test_client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200
    assert "Your cart is empty" in response.content.decode()

    # 2. Add product to cart with custom quantity (2)
    response = test_client.post(
        reverse("cart:add_to_cart", args=[p1.id]),
        {"quantity": "2"},
    )
    # Redirects to cart_detail
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")

    # Verify session state contains the correct item and quantity
    session = test_client.session
    assert session["cart"] == {str(p1.id): {"qty": 2}}

    # 3. Verify cart detail page displays the product
    response = test_client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200
    assert p1.name in response.content.decode()

    # 4. Update cart item quantity (3)
    response = test_client.post(
        reverse("cart:update_cart", args=[p1.id]),
        {"quantity": "3"},
    )
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")

    # Verify session updated
    session = test_client.session
    assert session["cart"] == {str(p1.id): {"qty": 3}}

    # 5. Clear the cart
    response = test_client.post(reverse("cart:clear_cart"))
    assert response.status_code == 302
    assert response.url == reverse("cart:cart_detail")

    # Verify session cart is cleared
    session = test_client.session
    assert session["cart"] == {}
