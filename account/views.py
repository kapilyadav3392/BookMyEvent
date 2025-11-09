from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from eventApp.models import Event

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        user = User.objects.create_user(
            username=username,
            password=password,
            role=role,
            phone=phone,
            address=address
        )

        return redirect("account:login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, "login.html", {"error": "Invalid credentials"})

        login(request, user)

        if user.role == "organizer":
            return redirect("account:event_manage")  
        else:  
            return redirect("account:dashboard")     

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("account:login")


@login_required
def dashboard_view(request):
    """Attendee dashboard"""
    upcoming_events = Event.objects.all()  
    return render(request, "dashboard.html", {"upcoming_events": upcoming_events})


@login_required
def event_manage_view(request):
    print("hello event")
    """Organizer dashboard"""
    if request.user.role != "organizer":
        return redirect("account:dashboard") 

    events = Event.objects.filter(organizer=request.user)
    return render(request, "eventmanage.html", {"events": events})