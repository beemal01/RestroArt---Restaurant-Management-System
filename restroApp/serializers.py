from rest_framework import serializers
from .models import Food, Cart, reservation

class FoodSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Food
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    food_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ["id", "food", "food_id", "quantity"]


class ReservationSerailizer(serializers.ModelSerializer):
    date = serializers.DateField(format="%m/%d/%Y")
    class Meta:
        model = reservation
        fields = '__all__'
        read_only_fields = ['user']







