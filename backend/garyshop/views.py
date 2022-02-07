from re import template
import re
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    # get the request in
    # do some logic with models in database
    # return a webpage to the user
    products = Product.objects.all()
    return render(request, 'index.html', {'products':products })

def product_individual(request, prodid):
    product = Product.objects.get(id = prodid)
    return render(request, 'product_individual.html', {'product':product})

class UserSignupView(CreateView):
    model = API_user
    form_class = UserSignupForm
    template_name = "user_register.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class UserLoginView(LoginView):
    template_name = 'login.html'

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def add_to_basket(request, prodid):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        Basket.objects.create(user_id = user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()

    product = Product.objects.get(id = prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id=product).first()
    if sbi is None:
        sbi = BasketItem(basket_id=basket, product_id=product).save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    
    return render(request, 'product_individual.html', {'product':product, 'added':True}) 

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(user_id = user, is_active=True).first()
    if basket is None:
        return render(request, 'basket.html', {'empty':True})
    else:
        sbi = BasketItem.objects.filter(basket_id = basket)
        if sbi.exists():
            return render(request, 'basket.html', {'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'basket.html', {'empty':True})

@login_required
def remove_item(request, sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect("/basket")
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity - 1
            basketitem.save()
        else:
            basketitem.delete()
    return redirect("/basket")

@login_required
def order(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return redirect('/')
    sbi = BasketItem.objects.filter(basket_id=basket)
    if not sbi.exists():
        return redirect('/')
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit = False)
            order.user_id = user
            order.basket_id = basket
            total  = 0.0
            for item in sbi:
                total += float(item.price())
            order.total_price = total 
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order': order, 'basket':basket, 'sbi':sbi})
        else:
            form = OrderForm()
            return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})

    else:
        form = OrderForm()
        return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})

@login_required
def previous_orders(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'previous_orders.html',{'orders':orders})