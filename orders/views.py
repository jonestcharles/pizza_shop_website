from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Prefetch
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import RegistrationForm
from .models import Category, Dish, Topping, OrderItem, Order

# Create your views here.
# all views take request as argument

def index(request):
    """
    Index View

    Loads the homepage. Redirects to login if not authenticated. Queries for
    Categories and Dishes, and renders the homepage, with full menu, if found.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    try:
        context = {
            "categories": Category.objects.all(),
            "dishes": Dish.objects.select_related('category').all()
        }

    except Category.DoesNotExist:
        raise Http404("Category not found")
    
    except Dish.DoesNotExist:
        raise Http404("Dish not found")

    return render(request, "orders/index.html", context)

def login_view(request):
    """
    Login View

    Renders login page. If login for is submitted, the view authenticates the user,
    and logs them in if found, redirecting to the homepage. If not found, prints
    an 'Invalid Credentials' message an displays the login page.
    """
    if request.method == "POST":
        username = request.POST["username"]
        raw_password = request.POST["password"]
        user = authenticate(request, username=username, password=raw_password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "orders/login.html", 
                {"message": "Invalid credentials"})
  
    return render(request, "orders/login.html")

def logout_view(request):
    """
    Logout View

    Logs the current user out, and redirects to the login page.
    """
    logout(request)
    return render(request, "orders/login.html", {"message": "Logged out"})

def register_view(request):
    """
    Registration View

    New user registration. This uses an extension of the built-in UserCreationForm
    called RegistrationForm to gather info such as first and last name, email, and
    2 passwords (identical) to validate the new user.

    Upon authentication, logs the user in. Before reirecting to the homepage, sends
    an email, in text and HTML, welcoming the new user.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # build and send email
            context = {"user": user}
            subject = "Welcome to Pinnochio's Pizza!"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email, ]
            html_message = render_to_string("orders/wel_email.html", context)
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, email_from, recipient_list, 
                html_message=html_message)

            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "orders/register.html", {"form": form})

    else:
        form = RegistrationForm()

        return render(request, "orders/register.html", {"form": form})

def add_to_cart(request):
    """
    Add to Cart View

    This view creates a new OrderItem from a form on the menu page. User must be
    authenticated to add an item to cart (should already be authenticated on
    homepage).

    Uses the current user, selected dish, quantity, size, and toppings (if 
    applicable) to create a new OrderItem object. The new OrderItem has no Order
    associated with it, indicating it is in a shopping cart.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    try:
        context = {
            "categories": Category.objects.all(),
            "dishes": Dish.objects.select_related('category').all(),
        }

        # get request data
        current_user = request.user
        item_dish_key = request.POST["dish"]
        item_size = request.POST["size"]
        item_quantity = request.POST["quantity"]

        # pull dish item from key, all dish objects already in QuerySet in context
        item_dish = context["dishes"].get(pk=item_dish_key)

        # create new OrderItem
        item = OrderItem(dish=item_dish, quantity=item_quantity, 
            size=item_size, user=current_user)
        item.save()

        # loops through toppings if ther, and if dish can have them, adding to OrderItem
        if item.dish.num_toppings > 0 and "toppings" in request.POST.keys():
            item_toppings = request.POST.getlist("toppings")
            item.toppings.add(*item_toppings)

        context["success"] = "Added to Cart!"

    # catch likely exceptions
    except KeyError:
        return render(request, "orders/error.html", {"message": "Invalid item"})
    
    except Category.DoesNotExist:
        raise Http404("Category not found")
    
    except Dish.DoesNotExist:
        raise Http404("Dishes not found")

    return render(request, "orders/index.html", context)

def cart(request):
    """
    Cart View

    Displays the shopping cart. Items in a user's shopping cart are all OrderItems
    associated witht he current user, and without an associated Order.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    # get cart items
    try:
        cart_items = OrderItem.objects.filter(user=request.user, order=None)

    except OrderItem.DoesNotExist:
        raise Http404("Order item does not exist")

    context = {
        "cart_items": cart_items
    }
    
    return render(request, "orders/cart.html", context)

def place_order(request):
    """
    Place Order View

    Creates a new Order and saves it to the database. All items in the shopping
    cart are added to a new Order by association. Upon successful order creation,
    a confirmation email (text or HTML) is sent to the user, containing basic
    order information. Redeirects to a thank you page.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    try:
        cart_items = OrderItem.objects.filter(user=request.user, order=None)
    
    except OrderItem.DoesNotExist:
        raise Http404("Order item does not exist")

    new_order = Order(user=request.user)
    new_order.save()

    # add OrderItems to new Order
    for item in cart_items:
        item.order = new_order
        item.save()

    context = {
        "order": new_order,
        "user": request.user
    }

    # build and send email
    subject = "Pinnochio's Pizza Order Confirmation"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email, ]
    html_message = render_to_string("orders/ty_email.html", context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, email_from, recipient_list, 
        html_message=html_message)

    return HttpResponseRedirect(reverse("thank_you", args=[new_order.pk]))

def thank_you(request, order_id):
    """
    Thank You View

    Uses the newly created Order to show a thank you page and order informaiton
    upon new order. Creates a url path /thankyou/<int:order.pk> (see urls.py).
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    try:
        order = Order.objects.get(pk=order_id)
    
    # catch potential exceptions
    except Order.DoesNotExist:
        raise Http404("Order does not exist")

    except OrderItem.MultipleObjectsReturned:
        return render(request, "orders/error.html", 
            {"message": "Invalid request - duplicate order ID"})
   
    context = {
        "order": order
    }

    return render(request, "orders/thankyou.html", context)

def delete_item(request):
    """
    Delete Item Request

    Deletes an Order Item from the shopping cart. Order Item is completely
    removed from the server.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    try:
        key = request.POST["key"]
    
    except KeyError:
        return render(request, "orders/error.html", {"message": "Invalid request"})

    try:
        item = OrderItem.objects.get(pk=key)
        item.delete()

    # catch potential exceptions
    except OrderItem.DoesNotExist:
        raise Http404("Order item does not exist")

    except OrderItem.MultipleObjectsReturned:
        return render(request, "orders/error.html", 
            {"message": "Invalid request - duplicate item"})

    return HttpResponseRedirect(reverse("cart"))
