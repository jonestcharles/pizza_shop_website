from django.contrib import admin

from .models import Category, Dish, Topping, Order, OrderItem

# Register your models here.
class OrderItemInstanceInline(admin.TabularInline):
    """
    Creates an inline view in the admin Orders Dashboard, allowing admin to
    view/modify all OrderItems in a given Order from same page.
    """
    model = OrderItem
    extra=0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Register Order with a custom list view and OrderItem inline
    """
    list_display = ('order_id', 'total', 'user', 'created')
    inlines = [OrderItemInstanceInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Register OrderItem with a custom list view
    """
    list_display = ('dish', 'total', 'user', 'created', 'order', 'size', 'quantity')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """
    Register Dish with a custom list view
    """
    list_display = ('name', 'category', 'small_price', 'large_price', 'num_toppings')

@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    """
    Register Topping with a custom list view
    """
    list_display = ('name', 'price', 'is_steak_and_cheese')

# register Category
admin.site.register(Category)
