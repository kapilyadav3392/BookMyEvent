from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, EventListAPIView, OrganizerEventListAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('events/', EventListAPIView.as_view(), name='api-events'),
    path('organizer/events/', OrganizerEventListAPIView.as_view(), name='api-organizer-events'),
]
