from django.urls import path
from .views import register_view, login_view, logout_view, dashboard_view, event_manage_view

app_name = "account"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('manage/', event_manage_view, name='event_manage'),
]
