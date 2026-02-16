import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billing_system.settings')
django.setup()

from billing.models import Product

products = [
    {"name": "Rice", "product_id": "P001", "stock": 100, "unit_price": 50.0, "tax_percentage": 5},
    {"name": "Sugar", "product_id": "P002", "stock": 200, "unit_price": 40.0, "tax_percentage": 5},
    {"name": "Oil", "product_id": "P003", "stock": 150, "unit_price": 120.0, "tax_percentage": 12},
    {"name": "Flour", "product_id": "P004", "stock": 100, "unit_price": 30.0, "tax_percentage": 5},
]

for p in products:
    Product.objects.update_or_create(product_id=p["product_id"], defaults=p)

print("Products seeded successfully!")
