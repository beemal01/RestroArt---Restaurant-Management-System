from django.contrib import admin
from .models import Food, Cart, reservation
# Register your models here.

admin.site.register(Food)
admin.site.register(Cart)
admin.site.register(reservation)