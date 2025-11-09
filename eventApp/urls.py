from django.urls import path
from . import views

urlpatterns = [
    path('create-event/', views.create_event, name='create_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('cancel/<int:event_id>/', views.cancel_event, name='cancel_event'),
    path("book/<int:event_id>/", views.book_event, name="book_event"),
    path("my-bookings/", views.attendee_bookings, name="attendee_bookings"),
    path("cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("booking/<int:booking_id>/delete/", views.delete_booking, name="delete_booking"),

    
]
