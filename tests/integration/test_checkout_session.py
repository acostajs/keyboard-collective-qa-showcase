import pytest
from django.urls import reverse
from django.test import Client
from unittest.mock import patch, MagicMock
from inventory.models import Category, Product


@pytest.mark.django_db
@patch("stripe.checkout.Session.create")
def test_checkout_and_session_creation(
    mock_stripe_create: MagicMock,
    test_client: Client,
    seed_data: tuple[Category, Product, Product, Product],
) -> None:
    """
    Integration test for cart checkout and Stripe checkout session creation.
    """
    category, p1, p2, p3 = seed_data

    # Mock the stripe session creation response
    class MockSession:
        url = "https://checkout.stripe.com/pay/cs_test_12345"
        id = "cs_test_12345"

    mock_stripe_create.return_value = MockSession()

    # 1. Add product to cart first (checkout requires a non-empty cart)
    test_client.post(
        reverse("cart:add_to_cart", args=[p1.id]),
        {"quantity": "1"},
    )

    # 2. Access checkout overview page
    response = test_client.get(reverse("cart:checkout"))
    assert response.status_code == 200
    assert p1.name in response.content.decode()

    # 3. Request a Stripe checkout session
    response = test_client.get(reverse("cart:create_checkout_session"))

    # Verify redirect to Stripe Checkout URL (Django's redirect yields 302 status code)
    assert response.status_code == 302
    assert response.url == "https://checkout.stripe.com/pay/cs_test_12345"

    # Verify Stripe was called with the correct parameters
    mock_stripe_create.assert_called_once()
    called_kwargs = mock_stripe_create.call_args[1]
    assert called_kwargs["mode"] == "payment"
    assert len(called_kwargs["line_items"]) == 1
    assert called_kwargs["line_items"][0]["quantity"] == 1
    assert (
        called_kwargs["line_items"][0]["price_data"]["unit_amount"]
        == p1.get_discounted_price()
    )
