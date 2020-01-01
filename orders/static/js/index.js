document.addEventListener('DOMContentLoaded', () => {
    
    const checkboxes = document.querySelectorAll('.form-check-input');
    const orderBtns = document.querySelectorAll('.reveal');
    const closeBtns = document.querySelectorAll('.close');

    // Checkbox onclick event
    //  Enforces maximum number of checkboxes that can be clicked, based on how
    //  many Toppings an OrderItem can have (based on Dish). Dish.num_toppings
    //  is passed to the id of the fieldset tag. When a checkbox is checked, if
    //  the checkbox count exceeds the number of Toppings that Dish is allowed,
    //  unchecks the box.

    checkboxes.forEach(box => {
        box.onclick = () => {
            var set = box.closest('.toppings-list')
            var checked = set.querySelectorAll('.form-check-input:checked').length;
            
            if (checked > parseInt(set.id, 10)) {
                box.checked = false;
            }
        }
    });

    // Order Now button onclick event
    //  Unhides the order form for each dish when clicked, allowing user to order

    orderBtns.forEach(btn => {
        btn.onclick = () => {
            var dishId = btn.dataset.form;

            const form = document.querySelector('#form-' + dishId);

            form.removeAttribute('hidden');
        }
    });

    // Close Button onclick event
    //  Hides the order form for a dish when the 'X' button is clicked
    
    closeBtns.forEach(btn => {
        btn.onclick = () => {
            var dishId = btn.dataset.form;

            const form = document.querySelector('#form-' + dishId);

            form.setAttribute('hidden', true);
        }
    });  
});

// addToCartValidate()
//  Validates the required number of checkboxes are checked before creating the
//  new OrderItem. Ensures the number of Toppings being submitted match the number
//  of toppings required for the given Dish. Only applies to pizzas - a 1 Topping
//  pizza cannot have no toppings, but a Sub can have 0 or more, while a Salad can
//  have none. If OrderItem is valid, submits the form to the server.

function addToCartValidate(form) {
    var numToppings = parseInt(form.dataset.toppings, 10);
    var category = parseInt(form.dataset.category, 10);

    if (numToppings > 0 && (category == 1 || category == 2)) {

        var set = form.querySelector('.toppings-list');
        var checked = set.querySelectorAll('.form-check-input:checked').length;
        var num = parseInt(set.id, 10);
        
        if (checked != num) {
            if (num == 1) {
                alert("Please Choose " + set.id + " topping");
            }

            else {
                alert("Please Choose " + set.id + " toppings");
            }

            return false;
        }
    }

    form.submit();
}
