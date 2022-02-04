from django.db import models
from django.contrib.auth.models import AbstractUser

class API_user(AbstractUser):
    pass

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits= 6 , decimal_places= 2, default= 0.0)
    image = models.FileField(upload_to='products', null=True)

class Basket(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(API_user, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class BasketItem(models.Model):
    id = models.IntegerField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default = 1)

    def price(self):
        return self.product_id.price * self.quantity

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)
    user_id = models.ForeignKey(API_user, on_delete=models.CASCADE)
    datetime_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits= 6 , decimal_places= 2, default= 0.0)
    shipping_addr = models.TextField(default="")