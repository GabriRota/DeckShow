from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.PositiveIntegerField()
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    img_profilo = models.ImageField(upload_to = 'img_profilo', default = 'img_profilo_default.jpg')
    nationality = models.CharField(max_length=2, blank=True, help_text="Codice ISO della nazione (es. IT, US, FR)")

    def __str__(self):
        return self.user.username

class Post(models.Model):
    CONDITION_CHOICES = [
        ('Mint', 'Mint'),
        ('Near mint', 'Near mint'),
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Light played', 'Light played'),
        ('Played', 'Played'),
        ('Poor', 'Poor'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=80)
    image_front = models.ImageField(upload_to='img_post')
    image_back = models.ImageField(upload_to='img_post')
    description = models.TextField(max_length=300)
    conditions = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    date_time = models.DateTimeField(default=datetime.now)
    n_of_like = models.IntegerField(default=0)
    n_of_wishlist = models.IntegerField(default=0)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user

