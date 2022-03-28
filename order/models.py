from pyexpat import model
from django.db import models
from shop.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=2)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_total_discount_item_price(self):
        return self.quantity * self.product.discount_price

    def get_final_price(self):
        if self.product.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    phone_number = models.CharField(blank=True, max_length=50)
    session_key = models.CharField(max_length=40, null=True)

    def __str__(self):
        return str([i for i in self.items.all()])
        # return f"order of {self.user.email}"

    @property
    def get_quantity(self):
        count = 0
        for item in self.items.all():
            count += item.quantity
        return count

    @property
    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_final_price()
        return total
