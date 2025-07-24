from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import TravelOption, Booking 
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .forms import ProfileUpdateForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def travel_list(request):
    travels = TravelOption.objects.all()

    t_type = request.GET.get("type")
    source = request.GET.get("source")
    destination = request.GET.get("destination")
    date = request.GET.get("date")

    if t_type:
        travels = travels.filter(travel_type__icontains=t_type)
    if source:
        travels = travels.filter(source__icontains=source)
    if destination:
        travels = travels.filter(destination__icontains=destination)
    if date:
        travels = travels.filter(date=date)

    booked_ids = Booking.objects.filter(user=request.user).values_list('travel_option_id', flat=True)

    return render(request, 'core/travel_list.html', {
        'travels': travels,
        'booked_ids': booked_ids
    })


@login_required
def book_trip(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)
    
    if request.method == "POST":
        Booking.objects.create(user=request.user, travel_option=travel, booking_date=timezone.now())
        messages.success(request, "Booking confirmed!")
        return redirect('my_bookings')

    return render(request, 'core/book.html', {'travel': travel})

@login_required
def book_trip(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)

    if request.method == "POST":
        num_seats = int(request.POST.get("num_seats", 1))

        if num_seats > travel.available_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('book_trip', pk=pk)

        total_price = num_seats * travel.price
        Booking.objects.create(
            user=request.user,
            travel_option=travel,
            num_seats=num_seats,
            total_price=total_price,
            status="Confirmed"
        )

        travel.available_seats -= num_seats
        travel.save()

        messages.success(request, "Booking confirmed!")
        return redirect('my_bookings')

    return render(request, 'core/book.html', {'travel': travel})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    for booking in bookings:
        print(f" ID: {booking.booking_id},User: {booking.user}, Travel: {booking.travel_option}, Seats: {booking.num_seats},price:{booking.total_price},date:{booking.booking_date}, Status: {booking.status}")
    return render(request, 'core/bookings.html', {'bookings': bookings})


@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = make_password(password)

        user.save()
        return redirect('home') 

    return render(request, 'core/profile.html')

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.delete()
    messages.success(request, "Booking cancelled.")
    return redirect('my_bookings')
