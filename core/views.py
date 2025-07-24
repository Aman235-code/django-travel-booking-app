from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import RegisterForm, LoginForm, ProfileUpdateForm, BookingForm
from .models import TravelOption, Booking


def home(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Account Created, Please Login', extra_tags='success')
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
                messages.add_message(request, messages.SUCCESS, 'Logged in successfully!', extra_tags='success')
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password.', extra_tags='danger')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged Out successfully!', extra_tags='success')
    return redirect('login')

@login_required
def travel_list(request):
    travels = TravelOption.objects.all()

    t_type = request.GET.get("type")
    source = request.GET.get("source")
    destination = request.GET.get("destination")
    date_input = request.GET.get("date")

    if t_type:
        travels = travels.filter(travel_type__icontains=t_type)

    if source:
        travels = travels.filter(source__icontains=source)

    if destination:
        travels = travels.filter(destination__icontains=destination)

    if date_input:
        try:
            date_obj = datetime.strptime(date_input, "%Y-%m-%d").date()
            travels = travels.filter(date_time__date=date_obj)
        except ValueError:
            pass 

    booked_ids = Booking.objects.filter(user=request.user).values_list('travel_option_id', flat=True)

    return render(request, 'core/travel_list.html', {
        'travels': travels,
        'booked_ids': booked_ids
    })


@login_required
def book_trip(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)

    if request.method == "POST":
        try:
            num_seats = int(request.POST.get("num_seats", 1))
            booking_date_str = request.POST.get("booking_date")

            booking_date_naive = datetime.strptime(booking_date_str, "%Y-%m-%dT%H:%M")
            booking_date = timezone.make_aware(booking_date_naive, timezone.get_current_timezone())

        except (ValueError, TypeError):
            messages.error(request, "Invalid input. Please enter valid date and number of seats.", extra_tags='danger')
            return redirect('book_trip', pk=pk)

        if num_seats > travel.available_seats:
            messages.error(request, "Not Enough Seats Available!", extra_tags='danger')
            return redirect('book_trip', pk=pk)

        if booking_date >= travel.date_time:
            messages.error(request, "Booking time must be before the scheduled travel time.", extra_tags='danger')
            return redirect('book_trip', pk=pk)

        if booking_date < timezone.now():
            messages.error(request, "Booking time cannot be in the past.", extra_tags='danger')
            return redirect('book_trip', pk=pk)

        total_price = num_seats * travel.price
        Booking.objects.create(
            user=request.user,
            travel_option=travel,
            num_seats=num_seats,
            total_price=total_price,
            status="Confirmed",
            booking_date=booking_date,
        )

        travel.available_seats -= num_seats
        travel.save()

        messages.success(request, "Booking Confirmed!", extra_tags='success')
        return redirect('my_bookings')
      

    return render(request, 'core/book.html', {'travel': travel})


@login_required
def book_travel(request, pk):
    travel = get_object_or_404(TravelOption, pk=pk)

    if request.method == 'POST':
        num_seats = int(request.POST.get('num_seats', 1))
        now = timezone.now()

        if now > travel.date_time:
            messages.error(request, "Cannot book for past travel!")
            return redirect('travel_list')

        if travel.available_seats < num_seats:
            messages.error(request, "Not enough seats available.")
            return redirect('travel_list')

        Booking.objects.create(
            user=request.user,
            travel_option=travel,
            num_seats=num_seats,
            total_price=num_seats * travel.price,
            status='Confirmed',
            booking_date=now
        )

        travel.available_seats -= num_seats
        travel.save()

        messages.success(request, "Booking Confirmed!")
        return redirect('my_bookings')

    return render(request, 'core/book_form.html', {'travel': travel})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
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
    travel_option = booking.travel_option
    travel_option.available_seats += booking.num_seats  
    travel_option.save()
    booking.delete()
    messages.error(request, 'Booking Cancelled!', extra_tags='danger')
    return redirect('my_bookings')
