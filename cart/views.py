from django.contrib import messages
from django.shortcuts import redirect, render
from .cart import Cart
from .forms import CheckoutForm
from order.utilities import checkout, notify_vendor, notify_customer

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                # Retrieve form data
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']

                # Simulate successful order creation
                order = checkout(request, first_name, last_name, email, phone, address, zipcode, place, cart.get_total_cost())

                # Clear the cart
                cart.clear()

                # Notify customer and vendor
                notify_customer(order)
                notify_vendor(order)

                # Redirect to success page
                messages.success(request, "Your order has been successfully placed!")
                return redirect('cart:success')
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Invalid form submission. Please check the fields.")
    else:
        form = CheckoutForm()

    # Handle cart updates
    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart:cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart:cart')

    # Render the cart page
    return render(request, 'cart/cart.html', {'form': form})


def success(request):
    return render(request, 'cart/success.html')
