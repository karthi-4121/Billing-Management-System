from django.contrib import admin
from .models import Product, Bill, BillItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_id", "name", "unit_price", "tax_percentage")
    search_fields = ("name", "product_id")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_email",
        "total_without_tax",
        "total_tax",
        "net_total",
        "rounded_total",
        "paid_amount",
        "balance",
        "created_at",
    )
    search_fields = ("customer_email",)
    list_filter = ("created_at",)


@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = (
        "bill",
        "product",
        "quantity",
        "unit_price",
        "purchase_price",
        "tax_amount",
        "tax_payable",
        "total_price",
    )
