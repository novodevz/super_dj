from django.db import models
from django.utils.text import slugify

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(
        unique=True,
        max_length=100,
    )

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)[:100]  # Truncate the slug if necessary
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(
        unique=True,
        max_length=100,
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="categories"
    )

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)[:100]  # Truncate the slug if necessary
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    image = models.CharField(
        max_length=255, blank=True, null=True
    )  # CharField to hold image URL

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]  # Truncate the slug if necessary
            # self.slug = f"{slug}-id{self.id}"  # Append id to the slug

        if not self.image:
            self.image = "default.jpg"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# pypl

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
