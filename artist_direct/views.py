from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.forms import ModelForm


from .models import User, Profile, Image

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["f_name", "l_name", "bio", "location", "genre", "instrument"]


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["f_name", "l_name", "bio", "location", "genre", "instrument"]


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image", "title", "description"]
        
        def save(self):
            image = super(ImageForm, self).save()
            return image




def index(request):
    return render(request, "artist_direct/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "artist_direct/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "artist_direct/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "artist_direct/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "artist_direct/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "artist_direct/register.html")


# Display create user profile form and post to db if valid
def create_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "artist_direct/create_profile.html", { "form": ProfileForm() })
    else:
        form = ProfileForm()
    return render(request, "artist_direct/create_profile.html", { "form": form })


# Display artist index
def artist_index(request):
    # For users with a profile list the profile alphbetical order
    users = User.objects.all()
    context = { "users": users }
    return render(request, "artist_direct/artist_index.html", context)


# Display individual profile for each artist
def artist_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user_id)
    context = {
        "f_name": profile.f_name,
        "l_name": profile.l_name,
        "bio": profile.bio,
        "location": profile.location,
        "genre": profile.genre,
        "instrument": profile.instrument,
        "profile_id": profile.id,
        "profile_user_id": profile.user.id,
        "current_user_id": request.user.id
    }
    return render(request, "artist_direct/artist_profile.html", context)

# Edit profile of artist
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.save()
            return HttpResponseRedirect(reverse("artist_profile", args=(profile_id,)))
    else:   
        form = EditProfileForm(instance=profile)
        context = {"form": form, "profile_id": profile_id}
        return render(request, "artist_direct/edit_profile.html", context)

#  Upload image
def image_upload(request):
    images = Image.objects.all()
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("Image saved")
    else:
        form = ImageForm()
    return render(request, "artist_direct/image_upload.html", {"form": form })

   


        





