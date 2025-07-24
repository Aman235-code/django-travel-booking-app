from django.contrib import admin
from django.urls import path
from core import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('travels/', views.travel_list, name='travel_list'),
    path('book/<int:pk>/', views.book_trip, name='book_trip'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path('profile/', views.profile_view, name='profile'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),
]
