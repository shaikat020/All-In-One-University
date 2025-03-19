from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from collections import OrderedDict
from django.contrib import messages
from .models import (
    CafeteriaMenu, BusRoute, BusSchedule, Faculty, Course, ClassSchedule, Club,
    Event, CampusBuilding, MealBooking
)
from .forms import MealBookingForm, RegistrationForm

# ---------------------
# ✅ Home Page View
# ---------------------
def index(request):
    return render(request, 'index.html')

# ---------------------
# ✅ Authentication Views (Login, Logout, Register)
# ---------------------
def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout_view(request):
    logout(request)
    return redirect('login')

# ✅ User Registration View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            messages.success(request, "Registration successful. Welcome!")
            return redirect('dashboard')  # Redirect to the dashboard after sign-up
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# ---------------------
# ✅ 1) Cafeteria Menus
# ---------------------
def cafeteria_weekly_view(request):
    menu_items = CafeteriaMenu.objects.all().order_by('day')
    day_groups = OrderedDict()
    for item in menu_items:
        if item.day not in day_groups:
            day_groups[item.day] = []
        day_groups[item.day].append(item)
    return render(request, 'cafeteria_multi_day.html', {'day_groups': day_groups})

@login_required
def create_meal_booking(request):
    if request.method == 'POST':
        form = MealBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('booking_success')
    else:
        form = MealBookingForm()
    return render(request, 'meal_booking.html', {'form': form})

def booking_success_view(request):
    return render(request, 'booking_success.html')

# ---------------------
# ✅ 2) Bus Routes & Schedules
# ---------------------
def bus_schedules_view(request):
    routes = BusRoute.objects.all()
    schedules = BusSchedule.objects.all()
    return render(request, 'bus_schedules.html', {'routes': routes, 'schedules': schedules})

# ---------------------
# ✅ 3) Class Schedules & Faculty Contacts
# ---------------------
@login_required
def class_schedules_view(request):
    schedules = ClassSchedule.objects.all()
    faculty = Faculty.objects.all()
    courses = Course.objects.all()
    return render(request, 'class_schedules.html', {'schedules': schedules, 'faculty': faculty, 'courses': courses})

@login_required
def add_class_schedule(request):
    return HttpResponse("Add class schedule page (Implement logic here).")

@login_required
def class_schedule_view(request):
    return HttpResponse("Class schedule page (Implement logic here).")

# ---------------------
# ✅ 4) Events & Clubs
# ---------------------
def events_view(request):
    clubs = Club.objects.all()
    events = Event.objects.all().order_by('event_date')
    return render(request, 'events.html', {'clubs': clubs, 'events': events})

# ---------------------
# ✅ 5) Campus Navigation
# ---------------------
def campus_map_view(request):
    buildings = CampusBuilding.objects.all()
    return render(request, 'campus_map.html', {'buildings': buildings})

def buildings_json(request):
    buildings_data = list(CampusBuilding.objects.all().values())
    return JsonResponse(buildings_data, safe=False)
