from django.db import models
from django.db.models.query import DateTimeField

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(db_index=True)
    slug = models.SlugField(unique=True)
    author = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    image = models.ImageField(blank=True)
    discount_percent = models.PositiveIntegerField(default=0)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Sách'
        verbose_name_plural = 'Sách'

    def __str__(self):
        return self.title

    def get_discount_price(self):
        if self.discount_percent > 0:
            return self.price * (100 - self.discount_percent) / 100
        return self.price
