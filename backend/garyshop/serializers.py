from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']

class BasketItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['product_id', 'product_name', 'quantity', 'price']


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemsSerializer(many=True, read_only=True, source='basketitems_set')

    class Meta:
        model = Basket
        fields = ['id', 'user_id', 'is_active', 'items']
        

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'basket_id', 'date_ordered', 'user_id']


class APIUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = API_user
        fields = ['id','email','username']

        