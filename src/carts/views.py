from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address 

from accounts.models import GuestEmail
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile

from .models import Cart
def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        'id': x.id,
        'url': x.get_absolute_url(),
        'name': x.name, 
        'price': x.price
        } 
        for x in cart_obj.products.all()
    ]
    # data = serializers.serialize('json', cart_obj.products.all())
    # jquery receives data in json, so [<object>, <object>, <object>] nor working
    cart_data = {
        'products': products,
        'subtotal': cart_obj.subtotal,
        'total': cart_obj.total,
        # 'productsData': data,
        }
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # print("cart ", cart_obj.user ,cart_obj.products.all())
    context = {
        "cart": cart_obj
    }
    return render(request, "carts/home.html", context)

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product already gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            print("item removed:", product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()

        if request.is_ajax():
            print('ajax request')
            json_data = {
                'added': added,
                'removed': not added,
                'cartItemCount': cart_obj.products.count(),
            }
            return JsonResponse(json_data, status=200)
            # return JsonResponse({"message": "Error 400"}, status=400) #Django Restful API
    return redirect("cart:home") 

def checkout_home(request):
    cart_obj, new_cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if new_cart_created or cart_obj.products.count() == 0:
        # cart not exist or empty cart, we do not proceed to check out
        return redirect("cart:home")

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_guest_profile_created = BillingProfile.objects.new_or_get(request)

    address_qs = None
    
    if billing_profile:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if shipping_address_id or billing_address_id:
            order_obj.save()

    if request.method == 'POST':
        'check order is done'
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect("cart:success")

    context = {
        "order": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs" : address_qs
    }
    return render(request, "carts/checkout.html", context)

def checkout_done(request):
    context = {}
    return render(request, "carts/checkout_done.html", context)