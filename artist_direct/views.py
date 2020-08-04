from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.forms import ModelForm
from django.db.models import Q

from .models import User, Profile, Image


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "f_name",
            "l_name",
            "bio",
            "location",
            "genre",
            "instrument",
            "video_url",
            "statement",
            "reviews",
        ]


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "f_name",
            "l_name",
            "bio",
            "location",
            "genre",
            "instrument",
            "video_url",
            "statement",
            "reviews",
        ]


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image", "title", "description"]



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
        type = request.POST["type"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "artist_direct/register.html",
                {"message": "Passwords must match."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "artist_direct/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        
        # According to choice of user type, user is redirected to appropriate page
        if type == "artist":
            return HttpResponseRedirect(reverse("create_profile"))
        else:
            return HttpResponseRedirect(reverse("artist_index"))
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
            return HttpResponseRedirect(reverse("artist_index"))
        else:
            return render(
                request, "artist_direct/create_profile.html", {"form": ProfileForm()}
            )
    else:
        form = ProfileForm()
    return render(request, "artist_direct/create_profile.html", {"form": form})


# Display artist index
def artist_index(request):
    # For users with a profile list the profile alphbetical order
    #users = User.objects.all()
    profiles = Profile.objects.all()
    #context = {"users": users}
    context = {"profiles": profiles}
    return render(request, "artist_direct/artist_index.html", context)


# Display individual profile for each artist
def artist_profile(request, user_id, newContext={}):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user_id)
    context = {
        "f_name": profile.f_name,
        "l_name": profile.l_name,
        "bio": profile.bio,
        "location": profile.location,
        "genre": profile.genre,
        "instrument": profile.instrument,
        "statement": profile.statement,
        "video_url": profile.video_url,
        "reviews": profile.reviews,
        "profile_id": profile.id,
        "profile_user_id": profile.user.id,
        "current_user_id": request.user.id,
    }
    context.update(newContext)
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
    user = request.user
    user_profile = Profile.objects.get(pk=user.id)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            # image = ImageForm(image_field=request.FILES['image'])
            form.save()
            context = {"form": form}
            response = artist_profile(request, user_profile.id, context)
            return response
            # return HttpResponseRedirect(reverse("artist_profile", args=(user_profile.id)))
    else:
        form = ImageForm()
    return render(request, "artist_direct/image_upload.html", {"form": form})


# Search models
def search(request):
    query = request.GET["query"]
    if query is not None:
        matches = (
            Q(f_name__icontains=query)
            | Q(l_name__icontains=query)
            | Q(bio__icontains=query)
        )
        profiles = Profile.objects.filter(matches).distinct()
        if profiles.count() != 0:
            return render(request, "artist_direct/artist_index.html", {"profiles": profiles})
        else:
            message = "There are no matches for your entry."     
            return render(request, "artist_direct/artist_index.html", {"message":message})

