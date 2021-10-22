from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, User
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')


# @method_decorator(login_required, name='dispatch')
class ProductView(View):
    def get(self, request):
        bedcover = Product.objects.filter(category='Bedcover')
        cushion = Product.objects.filter(category='Cushion')
        runner = Product.objects.filter(category='Runner')
        return render(request, 'app/home.html', {'Bedcover': bedcover, 'Cushion': cushion, 'Runner': runner})


# def product_detail(request):
#     return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'Product': product, 'item_already_in_cart': item_already_in_cart})


@login_required
def add_to_cart(request):
    userins = request.user
    user = User.objects.get(username=userins)
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discount_price)
                amount += tempamount
            total_amount = amount+shipping_amount
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': total_amount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discount_price)
                amount += tempamount
            data = {
                'quantity': c.quantity,
                'totalamount': amount+shipping_amount,
                'amount': amount
            }
            return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        if(c.quantity == 0):
            c.quantity = 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discount_price)
                amount += tempamount
            data = {
                'quantity': c.quantity,
                'totalamount': amount+shipping_amount,
                'amount': amount
            }
            return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]

        for p in cart_product:
            tempamount = (p.quantity*p.product.discount_price)
            amount += tempamount
        data = {
            'totalamount': amount+shipping_amount,
            'amount': amount
        }
        return JsonResponse(data)


def buy_now(request):
    return render(request, 'app/buynow.html')


# def profile(request):
#     return render(request, 'app/profile.html')
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            country = form.cleaned_data['country']
            phone = form.cleaned_data['phone']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode, country=country, phone=phone)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated')
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {"order_placed": op})


# def change_password(request):
#     return render(request, 'app/changepassword.html')


def bedcover(request, data=None):
    if data == None:
        bed = Product.objects.filter(category='Bedcover')
    elif data == 'below':
        bed = Product.objects.filter(
            category='Bedcover').filter(discount_price__lt=1000)
    elif data == 'above':
        bed = Product.objects.filter(
            category='Bedcover').filter(discount_price__gt=1000)
    return render(request, 'app/bedcover.html', {'Bedcover': bed})


# def login(request):
#     return render(request, 'app/login.html')


# def customerregistration(request):
#     return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Awesome!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    if add.exists() == False:
        return redirect('/profile/')
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    # print(cart_product)
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity*p.product.discount_price)
            amount += tempamount
        total_amount = amount+shipping_amount
        return render(request, 'app/checkout.html', {'add': add, 'totalamount': total_amount, 'cart_items': cart_items})
    else:
        return render(request, 'app/emptycart.html')


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")
