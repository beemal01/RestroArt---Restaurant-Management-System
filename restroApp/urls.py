
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path('menu/', views.menu, name="menu"),
    path('reservation/', views.reservation_page, name="reservation"),
    path('contact/', views.contact, name="contact"),
    path('api/homeview/', views.homeview.as_view(), name="homeview"),
    path('api/foodview/', views.foodview.as_view(), name="foodview"),
    path('api/foodlist/', views.foodlist.as_view(), name="foodlist"),
    path("api/cartview/", views.cartview.as_view(), name="cart-list-create"),
    path("api/reservationview/", views.reservationview.as_view(), name="reservationview"),
    path('api/cartview/<int:id>/', views.cartupdateview.as_view(), name="cart-update"),
    path('api/deleteview/<int:id>/', views.carddeleteview.as_view(), name="carddeleteview"),
    path('api/checkout/', views.checkoutview.as_view(), name="checkout"),
]
