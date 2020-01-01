# pizza_shop_website
Practice Web Development with Django, HTML, CSS, and Javascript (for Web Development Grad Class)

1. Menu

This app supports all menu items and options for Pinnochio's Pizza. These options
are supported by Django models stored on a db.sqlite3 database. Every type of order
is a Dish object. Each Dish has a name and a Category. Category is a separate
model, only consisting of a name, used ot organize Dishes. They are related by
a ForeignKeyField. Each Dish also has a small and large price. The small price may
be null, as Dishes with only 1 size default to large, though the user does not see
this. Dishes also have a number of toppings, indicating the maximum number of
toppings they can have, thereby creating differences between pizzas with different
topping quatities, for example. The third model describing the menu is Toppings.
Each Topping has a name, a ManyToManyField linking it to a Category, and a
BooleanField indicating whether or not the Topping is applied to the special case
of the Steak and Cheese Sandwich (this Dish is the only sandwich haing certain
Topping options.) Each Topping also has a price, as some cost extra. Refer to 
orders/models.py for code and documentation. Note for this app, a Special pizza
is one that contians 5 toppings.

The models are displayed via the path and view in urls.py and views.py for 'index'.
The index page loads all Dishes and Categories, diaplying options and prices to
the user. THe user must be authenticated to view the page (see below).

2. Adding Items

All items can be added to the database via the Django shell or the admin dashboard.
I added them via the Dashboard. All 3 models for the menu are registered in admin.py.
I used ModelAdmin objects for each model, besides Category, to display more info
about each instance on the Model dahsbaord, before clicking into an instance.

3. Registration, Login, Logout

THis app uses Django's built-in authentication system. All views besides Login,
Logout, and Register require authentication. Unauthenticated visitors are redirected
to the Login page (login.html). Login requires a username and password. Users are
authenticated and if successful, redirected to the homepage.

Registration is done with an extension of Django's UserCreationForm called RegistrationForm.
This object is in forms.py. This form class adds additional fields for first and
last name, as well as email address. This form is unpacked in register.html.

Logout acn be performed from any page beyond the authentication wall using a navbar
link. Logout logs the user out and redirects to the login page. For more info,
reference views.py and forms.py.

4. Shopping Cart

When on the homepage, users can create OrderItems and add them to their cart.
OrderItem is a fourth model in models.py. Each rder item is associated with a User
and a Dish. Further, each OrderItem has a size, wuantity, and a number of Toppings
associated with it. Lastly, each OrderItem has an Order object. This ForeignKeyField
can be Null, and initially OrderItems are created without an Order. OrderItems
whose Order field is Null are treated as items in that user's cart. The total is
calculated with a class method which uses the size to get the base cost from the
Dish object, and add all costs from Toppings (if the Dish is in the Subs Category,
Pizza Toppings are included in the base price). An OrderItem object is also given
datetime fields for the last edit and initial creation.

To order, the user clicks the Order Item button for a Dish. This reveals a form
where the User can enter a size, if there is an option, quantity, and Toppings, if
applicable. The form uses the num_toppings vlaue from the Dish to ensure that no
more than the allowed toppings are clicked, and that Pizza OrderItems are not
created with fewer than num_toppings (a 3 Topping pizza without 3 Toppings isn't 
allowed!). The code for this functionality is in static/index.js.

An added item goes to the view (in views.py) add_to_cart(), which creates a new
OrderItem, saves all data from the user and saves it to the DB. A success message
is then displayed on the homepage.

If a user uses the navbar to avigate to their cart, they are able to see all 
OrderItems in their cart. These are OrderItems with no Order, and are retrieved
in the view cart(). In the cart, a user can delete an item (not edit currently).
Deleteing an item call the view delete(), which fetches and removes the OrderItem.
All Dishes and Toppings are protected from the deletion.

5. Placing an Order

Orders are a fifth model in models.py. Each Order has an associated user, and a
unique ID (in addition to the primary key). This number is generated on initial
creation by overriding the inherited save() function. This could eventually be
a type of hash funciton, but now just uses the function generate_order_id(), in
models.py, to get a random 8 digit integer. Orders also have datetime fields for
last edit and initial creation. Order has a class method that gives the total for
the Order by summing the totals from each associated OrderItem.

Orders are created by submitting an Order from the cart. This option is only
displayed if OrderItems are in the cart. By reviewing all OrderItems and their prices,
along with the total Order price, the user confirms accuracy (items can be 
removed if needed). The place_order() view in views.py creates a new Order item,
then sets the Order field value in each OrderItem from the cart, removing them 
from the cart and building the order. The user is then redirected to a thank you
page (thankyou.html) where they see the details of their order (id, all items,
and the total).

6. Viewing Orders

The admin can view orders on the admin dashboard. admin.py makes this easier by
implementing ModelAdmin classes for OrderItem and Orders. For OrderItem, it inlines
all assocaited OrderItems to a given Order, making these viewable and editable from
the same page.

7. Personal Touch

For my personal touch, I chose to send email confirmations. Email confirmations
are sent to users upon placing an order and initial registration. This uses a 
Gmail account - detials to access that account are saved in environment variables
in settings.py. Other additional environament variables there setup the email
service (port, host, etc.). No dependencies are needed, this uses Django's core
mail library. For testing purpose, the same Gmail account was used for test users
to recieve emails.

When a user registers or places an Order (in the same view, place_order or register)
an email is sent. First, context is built to apss to the html email template (user
for the registration email, and the Order and user for the order confirmation). 
Then a subject line, recipient list (the current user's email) and the sending
email (environment variable) are created. The actual content is created by using 
the function render_to_string()
on the email template (wel_email.html or ty_email.html). Then a plain text 
message is made form that html message by calling the strip_tags() function. This
allows the plain text message to be made from the rendered html, meaning that Django
context is used to make the message and will be contained in the plain text. The
send_mail() function takes these variables as parameters, and sends both the plain
text and html message, allowing email clients that won't accept html to read
the message. The welcome email is a confirmation and welcome, and the order
confirmatin email contains Order details, like the thank you page.

8. Other Files

error.html is used to display certain error messages (for KeyError and MultipleObjectsReturned
exceptions). Other erros return 404 errors. See views.py.
