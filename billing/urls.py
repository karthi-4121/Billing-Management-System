from django.urls import path
from .views import dashboard, billing_page, history_view, bill_detail_view

urlpatterns = [
    path('', dashboard, name='dashboard'),  # opens first
    path('billing/', billing_page, name='billing'),
    path('history/<str:email>/', history_view, name='history'),
    path('bill/<int:bill_id>/', bill_detail_view, name='bill_detail'),
]
