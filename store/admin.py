from django.contrib import admin
from .models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 
    search_fields = ['name']
    
    list_per_page = 20

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'discount_percent', 'stock', 'available', 'category', 'created', 'updated']
    prepopulated_fields = {'slug': ('title',)} 
    list_editable = ['price', 'discount_percent', 'stock', 'available']
    list_filter = ['available', 'created', 'updated', 'category']
    search_fields = ['title', 'author', 'description']
    
    list_per_page = 50
