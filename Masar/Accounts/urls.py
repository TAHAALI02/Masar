from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.home, name='home'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # both roles
    path("", views.live_map, name="live_map"),
    path("alerts/", views.alerts, name="alerts"),
    path("trips/", views.trip_history, name="trip_history"),

    # fleet manager only
    path("reports/", views.reports, name="reports"),
    path("users/", views.user_list, name="user_list"),
    path("users/new/", views.user_create, name="user_create"),
    path("users/<int:pk>/toggle/", views.user_toggle_active, name="user_toggle_active"),

]