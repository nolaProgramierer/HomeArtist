from django.contrib import admin
from .models import User, Profile, Image, Comment

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Comment)


