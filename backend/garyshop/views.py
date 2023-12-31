from re import template
import re
from django import views
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import generics

# Create your views here.
def index(request):
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class BasketViewSet(viewsets.ModelViewSet):
  serializer_class = BasketSerializer
  queryset = Basket.objects.all()
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
      user = self.request.user # get the current user
      if user.is_superuser:
          return Basket.objects.all() # return all the baskets if a superuser requests
      else:
          # For normal users, only return the current active basket
          shopping_basket = Basket.objects.filter(user_id=user, is_active=True)
          return shopping_basket

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user # get the current user
        if user.is_superuser:
            return Order.objects.all() # return all the baskets if a superuser requests
        else:
            # For normal users, only return the current active basket
            orders = Order.objects.filter(user_id=user)
            return orders

class APIUserViewSet(viewsets.ModelViewSet):
    queryset = API_user.objects.all()
    serializer_class = APIUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] #No login is needed to access this route
    queryset = queryset = API_user.objects.all()

class AddBasketItemAPIView(generics.CreateAPIView):
    serializer_class = AddBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

class RemoveBasketItemAPIView(generics.CreateAPIView):
    serializer_class = RemoveBasketItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = BasketItem.objects.all()

class CheckoutAPIView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()