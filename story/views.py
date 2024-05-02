from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .ai import ai_res


# Create your views here.
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
            return render(request, "story/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "story/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "story/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "story/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "story/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def index(request):
    if request.method == 'POST':
        prompt = request.POST.get("prompt")
        res = ai_res(prompt)

        if not res:
            print("No response from ai")
        else:
            print("response is " , res)
        try:
            data = Response.objects.create(user=request.user, input=prompt, response=res)
            print("input added" , data)
        except:
            raise Exception
        
        return render(request, "story/index.html",{
            "res": res,
        })
    else:
        data = Response.objects.filter(user=request.user)
        print(data)
        return render(request, "story/index.html",{
            "datas": data[::-1]
        })



