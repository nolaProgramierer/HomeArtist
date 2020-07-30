from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"User: {self.username}, Email: {self.email}"

    pass


class Profile(models.Model):

    USA = "US"
    CANADA = "CN"
    EUROPE = "EU"

    LOCATION_CHOICES = [
        (USA, "United States"),
        (CANADA, "Canada"),
        (EUROPE, "Europe"),
    ]

    SOLO = "Solo"
    CHAMBER = "Chamber"
    MUSICAL_THEATER = "Musical Theater"

    GENRE_CHOICES = [
        (SOLO, "Solo"),
        (CHAMBER, "Chamber"),
        (MUSICAL_THEATER, "Musical_Theater"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="user_profile"
    )
    f_name = models.CharField(max_length=24, blank=True)
    l_name = models.CharField(max_length=24, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(
        max_length=2, choices=LOCATION_CHOICES, default=USA, blank=True
    )
    genre = models.CharField(
        max_length=24, choices=GENRE_CHOICES, default=SOLO, blank=True
    )
    instrument = models.CharField(max_length=24, blank=True)

    def __str__(self):
        return f"User Profile: {self.f_name}, {self.l_name}, Bio:  {self.bio}, Resides:{self.location}, Genre: {self.genre}, Instrument: {self.instrument}"

