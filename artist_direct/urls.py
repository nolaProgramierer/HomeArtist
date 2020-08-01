from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_profile", views.create_profile, name="create_profile"),
    path("artist_index", views.artist_index, name="artist_index"),
    path("artist_profile/<int:user_id>", views.artist_profile, name="artist_profile"),
    path("edit_profile/<int:profile_id>", views.edit_profile, name="edit_profile"),
    path("image_upload", views.image_upload, name="image_upload"),
   
]
