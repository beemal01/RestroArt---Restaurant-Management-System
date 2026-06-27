from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('cart/', views.cart, name="cart"),
    path('api/signupview/', views.signupview.as_view(), name="signupview"),
    path('api/signinview/', views.signinview.as_view(), name="signinview"),
    path('api/logoutview/', views.logoutview.as_view(), name="logoutview"),
]
