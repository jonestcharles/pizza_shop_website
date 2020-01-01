from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("cart", views.cart, name="cart"),
    path("place_order", views.place_order, name="place_order"),
    path("thankyou/<int:order_id>", views.thank_you, name="thank_you"),
    path("delete_item", views.delete_item, name="delete_item")
]
