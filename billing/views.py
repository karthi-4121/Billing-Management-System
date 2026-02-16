from django.shortcuts import render, get_object_or_404
from django.db import transaction
from decimal import Decimal
import math
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, Bill, BillItem
from .services import calculate_denominations

def dashboard(request):
    return render(request, "billing/dashboard.html")

@transaction.atomic 
def billing_page(request):
    products = Product.objects.all()
    denominations = [500, 100, 50, 20, 10, 5, 2, 1]
    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        paid_amount_raw = request.POST.get("paid_amount")

        if not email or not paid_amount_raw:
            error = "Email and paid amount are required."
        else:
            try:
                paid_amount = Decimal(paid_amount_raw)
            except:
                error = "Paid amount must be a valid number."

        product_ids = request.POST.getlist("product[]")
        quantities = request.POST.getlist("qty[]")

        if not error and (not product_ids or not quantities):
            error = "Please select at least one product."

        if not error:
            total_without_tax = Decimal("0.00")
            total_tax = Decimal("0.00")

            bill = Bill.objects.create(
                customer_email=email,
                paid_amount=paid_amount
            )

            items_data = []

            for pid, qty in zip(product_ids, quantities):
                try:
                    product = Product.objects.get(product_id=pid)
                    qty = int(qty)
                except:
                    error = f"Invalid product or quantity: {pid}"
                    break

                purchase_price = Decimal(
                    request.POST.get(f"purchase_price_{pid}", product.unit_price)
                ) * qty

                tax_amount = purchase_price * (product.tax_percentage / 100)
                total_price = purchase_price + tax_amount

                total_without_tax += purchase_price
                total_tax += tax_amount

                items_data.append({
                    "product": product,
                    "quantity": qty,
                    "unit_price": product.unit_price,
                    "purchase_price": purchase_price,
                    "tax_amount": tax_amount,
                    "total_price": total_price
                })

            if not error:
                net_total = total_without_tax + total_tax
                rounded_total = Decimal(math.floor(net_total))
                balance = paid_amount - rounded_total
                tax_ratio = rounded_total / net_total if net_total > 0 else 1

                bill.total_without_tax = total_without_tax
                bill.total_tax = total_tax
                bill.net_total = net_total
                bill.rounded_total = rounded_total
                bill.balance = balance
                bill.save()

                for data in items_data:
                    BillItem.objects.create(
                        bill=bill,
                        product=data["product"],
                        quantity=data["quantity"],
                        unit_price=data["unit_price"],
                        purchase_price=data["purchase_price"],
                        tax_amount=data["tax_amount"],
                        tax_payable=data["tax_amount"] * tax_ratio,
                        total_price=data["total_price"] * tax_ratio
                    )

                denomination = calculate_denominations(balance)
                send_invoice_email(bill, denomination)

                return render(request, "billing/summary.html", {
                    "bill": bill,
                    "denomination": denomination
                })

    return render(request, "billing/billing.html", {
        "products": products,
        "denominations": denominations,
        "error": error
    })


def send_invoice_email(bill, denomination):
    subject = f"Invoice - Bill #{bill.id}"
    message = f"Dear Customer,\n\nYour invoice:\n\nEmail: {bill.customer_email}\n\nItems:\n"

    for item in bill.items.all():
        message += (
            f"{item.product.name} | Qty: {item.quantity} | "
            f"Unit Price: {item.unit_price} | Purchase Price: {item.purchase_price} | "
            f"Tax(Item): {item.tax_amount:.2f} | Tax(Payable): {item.tax_payable:.2f} | "
            f"Total: {item.total_price:.2f}\n"
        )

    message += (
        f"\nTotal w/o Tax: {bill.total_without_tax}\n"
        f"Total Tax: {bill.total_tax}\n"
        f"Net Total: {bill.net_total}\n"
        f"Rounded Total: {bill.rounded_total}\n"
        f"Paid Amount: {bill.paid_amount}\n"
        f"Balance: {bill.balance}\n\n"
    )

    message += "Balance Denominations:\n"
    for k, v in denomination.items():
        message += f"{k} : {v}\n"

    message += "\nThank you for shopping with us!"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [bill.customer_email],
        fail_silently=False
    )


def history_view(request, email):
    bills = Bill.objects.filter(customer_email=email).order_by('-created_at')
    return render(request, "billing/history.html", {
        "bills": bills,
        "email": email
    })


def bill_detail_view(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, "billing/bill_detail.html", {"bill": bill})
