from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User
from datetime import datetime, date
import random

def generate_order_id():
    """
    Generates a random 128-bit number, then returns the last 8 digits as an
    order id
    """
    num = random.getrandbits(128)
    return num % 100000000

# Create your models here.
class Category(models.Model):
    """
    Category Model

    A Category models a set of dishes, i.e. Sandwiches, Pizzas, etc. Only field
    is name.
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Dish(models.Model):
    """
    Dish Model

    A Dish is a member of a category - an option on the menu. A Dish has a name,
    an associated Category, a price for small and large sizes (could be 0 if size
    not allowed), and an allowed number of Toppings.
    """
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
        related_name="dishes")
    small_price = models.DecimalField(max_digits=5, decimal_places=2, 
        null=True, blank=True)
    large_price = models.DecimalField(max_digits=5, decimal_places=2)
    num_toppings = models.IntegerField(default=0)

    def __str__(self):
        if self.small_price:
            return f"{self.name}: Small: ${self.small_price} Large: ${self.large_price}"

        return f"{self.name}: ${self.large_price}"

class Topping(models.Model):
    """
    Toppings Model

    Pizza and Sub toppings. Each Topping has a name, one or more associated Categories
    indicating which Dish types it can be used with, a price, if applicable, and 
    a boolean for the special case of a Steak and Cheese Sandwich.
    """
    name = models.CharField(max_length=64)
    category = models.ManyToManyField(Category, related_name="toppings")
    is_steak_and_cheese = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    """
    Orders Model

    An Order has an associated User, an 8-digit ID, and a timestamp for datetime
    last updated, and created.
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    order_id = models.IntegerField(default=-1, null=True, blank=True, editable=False)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"Order #{self.order_id}"

    def save(self, *args, **kwargs):
        """
        Generates a new order_id if this is the first time being saved to the DB
        """
        if not self.pk:
            self.order_id = generate_order_id()

        super(Order, self).save(*args, **kwargs)
    
    def total(self):
        """
        Returns the Order's total - the sum of the total of each OrderItem
        """
        total = Decimal('0.00').quantize(Decimal('0.01'))

        for item in self.items.all():
            total += Decimal(item.total()).quantize(Decimal('0.01'))

        return str(total)

class OrderItem(models.Model):
    """
    Order Item Model

    An OrderItem that is in an Order or a User's cart. If Order is Null, then the
    OrderItem is in the shopping cart. EachOrderItem has a Dish, a quantity, a size
    a User, a set of Toppings (could be none), and timestamps for datetime last
    modified and original creation.
    """
    LARGE = "LG"
    SMALL = "SM"

    size_choices = [
        (LARGE, "Large"),
        (SMALL, "Small")
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", 
        blank=True, null=True)
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, related_name="orderitem")
    quantity = models.IntegerField(default=1)
    size = models.CharField(choices=size_choices, max_length=2)
    toppings = models.ManyToManyField(Topping, related_name="items", blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="items", default=1)

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f"{self.dish.category}, {self.dish.name}, Quantity: {self.quantity}, Total: ${self.total()}"
    
    def total(self):
        """
        Total OrderItem price is a function of size, and the price of any added
        Toppings
        """
        if self.size == self.LARGE:
            price = self.dish.large_price

        else:
            price = self.dish.small_price
        
        if self.dish.category.pk == 3:
            for topping in self.toppings.all():
                price += topping.price

        total = (Decimal(price) * Decimal(self.quantity)).quantize(Decimal('0.01'))
        return str(total)
