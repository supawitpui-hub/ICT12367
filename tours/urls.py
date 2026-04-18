from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_trips, name='search_trips'),
    path('booking/<str:package_id>/', views.booking_view, name='booking_view'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('payment/<int:booking_id>/', views.payment_view, name='payment_view'),
    path('confirm-payment/<int:booking_id>/', views.confirm_payment, name='confirm_payment'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('ticket/<int:booking_id>/', views.booking_ticket, name='booking_ticket'),
    path('contact/', views.contact_view, name='contact'),
]