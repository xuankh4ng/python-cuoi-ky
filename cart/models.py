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
        return self.quantity * self.book.get_discount_price()

    def __str__(self):
        return f"{self.quantity} x {self.book.title} trong giỏ {self.cart.user.username}"
    
    class Meta:
        verbose_name = 'Mục Giỏ hàng'
        verbose_name_plural = 'Mục Giỏ hàng'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=0)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=0) 
    
    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"