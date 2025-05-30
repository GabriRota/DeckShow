from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_user = models.PositiveIntegerField()
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=30, blank=True)
    img_profilo = models.ImageField(upload_to='img_profilo', default='img_profilo_default.jpg')
    nationality = models.CharField(max_length=2, blank=True, help_text="Codice ISO della nazione (es. IT, US, FR)")
    seguiti = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    wishlist = models.ManyToManyField('Post', related_name='wishlisted', blank=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=80)
    image_front = models.ImageField(upload_to='img_post')
    image_back = models.ImageField(upload_to='img_post')
    description = models.TextField(max_length=300)
    conditions = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    date_time = models.DateTimeField(default=datetime.now)
    n_of_like = models.IntegerField(default=0)
    n_of_wishlist = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked', blank=True)
    wishlisted_by = models.ManyToManyField(User, related_name='wishlisted', blank=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
