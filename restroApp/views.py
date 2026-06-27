from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import *
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .tasks import send_conformation, reservation_seat
from rest_framework import filters
from .pagination import Mypagination

# Create your views here.


def index(request):
    return render(request, "index.html")

def menu(request):
    return render(request, "menu.html")

def reservation_page(request):
    return render(request, "reservation.html")

def contact(request):
    return render(request, "contact.html")


class homeview(generics.ListAPIView):
    queryset = Food.objects.all()[:6]
    serializer_class = FoodSerializer

class foodlist(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'show_title', 'food_category', 'chef_tags']
    pagination_class = Mypagination

    @method_decorator(cache_page(60 * 60 * 2, key_prefix = 'foodlist'))
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class foodview(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [IsAdminUser]


class cartview(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Cart.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        food_id = serializer.validated_data["food_id"]
        qty = serializer.validated_data.get("quantity", 1)

        existing = Cart.objects.filter(user=self.request.user, food_id=food_id).first()
        if existing:
            existing.quantity += qty
            existing.save()
        else:
            serializer.save(user=self.request.user, food_id=food_id)
    

class cartupdateview(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class checkoutview(generics.GenericAPIView):
    throttle_scope = 'checkout'
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Build email content from cart items BEFORE deleting
        item_text = ''
        total = 0
        for item in cart_items:
            semi_total = item.food.price * item.quantity
            total += semi_total
            item_text += f'-{item.food.title} (x{item.quantity}) Rs.{semi_total} \n'

        # Send confirmation email with pre-computed data
        send_conformation.delay(item_text, total, request.user.email, request.user.username)

        # Clear the cart after checkout
        cart_items.delete()

        return Response({"message": "Order placed successfully! Check your email for confirmation."}, status=status.HTTP_200_OK)


class carddeleteview(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    
class reservationview(generics.CreateAPIView):
    throttle_scope = 'reservation'
    serializer_class  =  ReservationSerailizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)

        if response.status_code == 201:
            # Get the newly created reservation
            reserve = reservation.objects.filter(user=request.user).last()
            if reserve:
                reservation_seat.delay(
                    reserve.full_name,
                    reserve.date,
                    reserve.time,
                    reserve.guest,
                    request.user.email
                )

        return response
    