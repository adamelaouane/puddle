from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    image = models.ImageField(
        upload_to='profile_images/',
        default='profile_images/default.png',
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"