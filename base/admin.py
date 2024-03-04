from django.contrib import admin

from .models import Category, Department, Order, OrderItem, Product

# Register your models here.

admin.site.register([Department, Category, Product, Order, OrderItem])
