from django.contrib import admin
from .models import OrderBook, Order


@admin.register(OrderBook)
class OrderBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'order', 'quantity', 'price', 'book_title']
    list_filter = [ 'quantity', 'price', 'book_title']




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_date', 'total_amount', 'status']
    list_filter = ['user', 'order_date', 'total_amount', 'status']


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user']
#     list_filter = ['user', 'books']
