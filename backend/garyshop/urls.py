from ast import increment_lineno
from django.contrib import admin
from django.urls import path, include
from garyshop import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import *
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'basket', views.BasketViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'users', views.APIUserViewSet)

urlpatterns = [
    path('', views.index, name="homepage"),
    path('products/<int:prodid>', views.product_individual, name="individual product"),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(template_name='login.html', authentication_form=UserLoginForm), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('addbasket/<int:prodid>', views.add_to_basket, name="add_basket"),
    path('basket/', views.show_basket, name='show_basket'),
    path('removeitem/<int:sbi>', views.remove_item, name="remove_item"),
    path('order/', views.order, name="order"),
    path('orderhistory/', views.previous_orders, name="order_history"),
    path('apiregister/', views.UserRegistrationAPIView.as_view(), name="api_register"),
    path('apiadd/', views.AddBasketItemAPIView.as_view(), name="api_add_to_basket"),
    path('apiremove/', views.RemoveBasketItemAPIView.as_view(), name="api_remove_from_basket"),
    path('apicheckout/', views.CheckoutAPIView.as_view(), name="api_checkout"),
    path('api/', include(router.urls)),
]