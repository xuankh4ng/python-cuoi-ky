from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/delete/<int:item_id>/", views.cart_delete, name="cart_delete"),
    path("cart/update/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("invoice/<int:order_id>/", views.order_detail, name="order_detail"),
    path("history/", views.order_history, name="order_history"),
]
