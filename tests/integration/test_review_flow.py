import pytest
from django.urls import reverse
from django.test import Client
from account.models import Account
from inventory.models import Category, Product
from cart.models import Order, OrderItem
from review.models import Review


@pytest.mark.django_db
def test_user_review_flow(
    test_client: Client,
    order_user: Account,
    seed_data: tuple[Category, Product, Product, Product],
) -> None:
    """
    Integration test for user review flow:
    1. Log in the user.
    2. Add a purchase record in the database for the user.
    3. Submit a product review.
    4. Verify the database contains the review.
    5. Verify the product detail page displays the review message.
    """
    category, p1, p2, p3 = seed_data

    # 1. Log in the user
    test_client.force_login(order_user)

    # 2. Add purchase record (Order and OrderItem) so user is authorized to review
    order = Order.objects.create(user=order_user, total_cents=p1.price)
    OrderItem.objects.create(
        order=order, product=p1, quantity=1, unit_price_cents=p1.price
    )

    # 3. Submit a product review
    response = test_client.post(
        reverse("review:review_submit", kwargs={"product_id": p1.id}),
        data={"rating": 5, "message": "Superb product, very satisfied!"},
    )

    # Verify redirection to product page
    assert response.status_code == 302
    assert response.url == reverse("inventory:product", kwargs={"product_id": p1.id})

    # 4. Verify review in the database
    review = Review.objects.get(user=order_user, product=p1)
    assert review.rating == 5
    assert review.message == "Superb product, very satisfied!"

    # 5. Verify the product detail page displays the review message
    response = test_client.get(
        reverse("inventory:product", kwargs={"product_id": p1.id})
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert "Superb product, very satisfied!" in content
