import pytest
from django.urls import reverse
from django.test import Client
from inventory.models import Category, Product


@pytest.mark.django_db
def test_catalog_search_and_filter(
    test_client: Client, seed_data: tuple[Category, Product, Product, Product]
) -> None:
    """
    Integration test for catalog searching and filtering views.
    """
    category, p1, p2, p3 = seed_data

    # 1. Access the main catalog index
    response = test_client.get(reverse("inventory:index"))
    assert response.status_code == 200
    assert "Keychron Q1" in response.content.decode()

    # 2. Search for "MX Master"
    response = test_client.get(reverse("inventory:results"), {"search": "MX Master"})
    assert response.status_code == 200
    content = response.content.decode()
    assert "MX Master 3S" in content
    assert "Keychron Q1" not in content

    # 3. Filter products on category page by discount
    response = test_client.get(
        reverse("inventory:category", args=[category.id]),
        {"filter_criteria": ["discount_percentage"]},
    )
    assert response.status_code == 200
    content = response.content.decode()
    # Keychron Q1 is discounted (10%) -> should be present
    assert "Keychron Q1" in content
    # MX Master 3S has no discount -> should not be present
    assert "MX Master 3S" not in content
