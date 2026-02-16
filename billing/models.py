from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, null=True)
    product_id = models.CharField(max_length=100, unique=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.name} ({self.product_id})"


class Bill(models.Model):
    customer_email = models.EmailField()
    total_without_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    net_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rounded_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Bill #{self.id} - {self.customer_email}"


class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items', null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    quantity = models.PositiveIntegerField(null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    tax_payable = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
