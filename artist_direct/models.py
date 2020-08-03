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

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_profile"
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
    video_url = models.URLField(blank=True)
    statement = models.CharField(max_length=250, blank=True)
    reviews = models.TextField(blank=True)

    @property
    def full_name(self):
        "Returns user's full name"
        return "%s %s" % (self.f_name, self.l_name)

    def __str__(self):
        return f"User Profile: {self.f_name}, {self.l_name}, Bio:  {self.bio}, Resides:{self.location}, Genre: {self.genre}, Instrument: {self.instrument}"

    class Meta:
        ordering = ["l_name"]


class Image(models.Model):
    image = models.ImageField(upload_to="img")
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="image_profile", default=1
    )

    def __str__(self):
        return f"Image title: {self.title} Description: {self.description} Image Profile User: {self.profile.user.username}"

