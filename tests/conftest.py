import os
import pytest
from faker import Faker
from inventory.models import Category, Product

# Set dummy environment variables for tests
os.environ.setdefault("STRIPE_SECRET_KEY", "sk_test_mock")
os.environ.setdefault("STRIPE_WEBHOOK_SECRET", "whsec_mock")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def fake_user() -> dict[str, str]:
    """
    Generate fake user registration data.
    """
    fake = Faker()
    return {
        "username": fake.user_name()[:30],
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password1": "SecurePassword123!",
        "password2": "SecurePassword123!",
        "address_line1": fake.street_address(),
        "address_line2": fake.secondary_address(),
        "city": fake.city(),
        "postal_code": "K1A 0B1",
        "country": "Canada",
    }


@pytest.fixture
def seed_data(db) -> tuple[Category, Product, Product, Product]:
    """
    Seed categories and products for testing catalog searching, sorting, filtering,
    and shopping cart operations.
    """
    cat = Category.objects.create(
        name="Keyboards",
        description="Premium Mechanical Keyboards",
        image="categories/keyboard.png",
    )

    # 1. Product 1: In stock, discounted
    p1 = Product.objects.create(
        name="Keychron Q1",
        description="Aluminum custom mechanical keyboard",
        quantity=5,
        price=15000,
        category=cat,
        discount_percentage=10,
        image="products/q1.png",
    )

    # 2. Product 2: In stock, regular price
    p2 = Product.objects.create(
        name="MX Master 3S",
        description="Wireless ergonomic office mouse",
        quantity=10,
        price=9900,
        category=cat,
        discount_percentage=0,
        image="products/mx.png",
    )

    # 3. Product 3: Out of stock
    p3 = Product.objects.create(
        name="Cable Organizer",
        description="Desk cable organizer",
        quantity=0,
        price=1500,
        category=cat,
        discount_percentage=0,
        image="products/cable.png",
    )

    return cat, p1, p2, p3
