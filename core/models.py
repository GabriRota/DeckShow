from django.db import models
from django.contrib.auth import get_user_model

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
