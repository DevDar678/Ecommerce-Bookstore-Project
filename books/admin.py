from django.contrib import admin
from .models import Book, Order, CashOnDeliveryOrder, Cart, CartItem, Category
@admin.register(CashOnDeliveryOrder)
class CashOnDeliveryOrderAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "postal_code", "phone_number", "created_at")
    search_fields = ("name", "city", "postal_code", "phone_number")

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'book_available')
    list_filter = ('category', 'book_available')
    search_fields = ('title', 'author')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "book", "quantity")
    
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Category)
