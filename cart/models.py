from django.db import models
from django.contrib.auth.models import User
from store.models import Book

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Giỏ hàng'
        verbose_name_plural = 'Giỏ hàng'

    def __str__(self):
        return f"Giỏ hàng của {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f"{self.quantity} x {self.book.title} trong giỏ {self.cart.user.username}"
    
    class Meta:
        verbose_name = 'Mục Giỏ hàng'
        verbose_name_plural = 'Mục Giỏ hàng'
