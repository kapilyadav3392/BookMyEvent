from django.urls import path
from .views import (
    CreateEventAPI,
    EditEventAPI,
    DeleteEventAPI,
    BookEventAPI,
    AttendeeBookingsAPI,
    CancelBookingAPI
)

urlpatterns = [
    path("event/create/", CreateEventAPI.as_view()),
    path("event/<int:event_id>/edit/", EditEventAPI.as_view()),
    path("event/<int:event_id>/delete/", DeleteEventAPI.as_view()),

    path("event/<int:event_id>/book/", BookEventAPI.as_view()),
    path("attendee/bookings/", AttendeeBookingsAPI.as_view()),
    path("booking/<int:booking_id>/cancel/", CancelBookingAPI.as_view()),
]