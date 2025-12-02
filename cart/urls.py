from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:book_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/increase/<int:item_id>/", views.cart_increase, name="cart_increase"),
    path("cart/decrease/<int:item_id>/", views.cart_decrease, name="cart_decrease"),
    path("cart/delete/<int:item_id>/", views.cart_delete, name="cart_delete"),
]
