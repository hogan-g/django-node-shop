from re import template
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

def add_to_basket(request, prodid):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if not basket:
        basket = Basket(user_id = user).save()

    product = Product.objects.get(id = prodid)
    sbi = BasketItem.objects.filter(basket_id=basket, product_id=product).first()
    if sbi is None:
        sbi = BasketItem(basket_id=basket, product_id=product).save()
    else:
        sbi.quantity = sbi.quantity+1
        sbi.save()
    
    return render(request, 'product_individual.html', {'product':product, 'added':True}) 
