from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Food(models.Model):
    image = models.ImageField(upload_to='menu/')  
    title = models.CharField(max_length=100)
    show_title = models.CharField(max_length=30)
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    old_price = models.FloatField(default=0, validators=[MinValueValidator(0)], null=True, blank=True)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.CharField(max_length=500)
    tags = models.CharField(max_length=200, help_text='Comma-separated tags')
    chef_tags = models.CharField(max_length=30, blank=True, null=True)
    food_category = models.CharField(max_length=30, blank=True, null=True)
    cook_time = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    calory = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(9999)])

    def __str__(self):
        return self.title
    

class Cart(models.Model):
        user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="cart"
        )
        food = models.ForeignKey(Food, on_delete=models.CASCADE)
        quantity = models.PositiveIntegerField(default=1)

        class Meta:
             unique_together = ('user', 'food')

        def __str__(self):
            return f"{self.user.username} - {self.food.title} ({self.quantity})"
        

class reservation(models.Model):
    PEOPLE_CHOICES = [
        ("1", "1 Person"),
        ("2", "2 People"),
        ("3-4", "3 - 4 People"),
        ("5-6", "5 - 6 People"),
        ("7-10", "7 - 10 People"),
        ("10+", "10+ People"),
    ]

    TIME_CHOICES = [
        ("09:00 AM", "09:00 AM"),
        ("10:00 AM", "10:00 AM"),
        ("11:00 AM", "11:00 AM"),
        ("12:00 PM", "12:00 PM"),
        ("01:00 PM", "01:00 PM"),
        ("02:00 PM", "02:00 PM"),
        ("06:00 PM", "06:00 PM"),
        ("07:00 PM", "07:00 PM"),
        ("08:00 PM", "08:00 PM"),
        ("09:00 PM", "09:00 PM"),
        ("10:00 PM", "10:00 PM"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE
        )
    full_name = models.CharField(max_length=100)
    number = models.CharField(max_length=20)
    email = models.EmailField()
    guest = models.CharField(choices=PEOPLE_CHOICES)
    date = models.DateField()
    time = models.CharField(choices=TIME_CHOICES)
    special_request = models.TextField(blank=True, null=True)

    def __str__(self):
         return f' {self.full_name} -Booked Date: {self.date} - Time: {self.time}'
    

