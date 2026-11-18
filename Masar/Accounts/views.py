from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm



from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import UserCreateForm
from .models import User
from .permissions import BOTH, MANAGER_ONLY, role_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect("live_map")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next")
            # Only follow "next" if it points to our own site (prevents open redirects)
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("live_map")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("login")







# ---------- Both roles ----------
@role_required(BOTH)
def live_map(request):
    return render(request, "live_map.html")


@role_required(BOTH)
def alerts(request):          # view alerts, acknowledge, add notes (built later)
    return render(request, "alerts.html")


@role_required(BOTH)
def trip_history(request):    # placeholder
    return render(request, "trip_history.html")


# ---------- Fleet manager only ----------
@role_required(MANAGER_ONLY)
def reports(request):
    return render(request, "reports.html")


@role_required(MANAGER_ONLY)
def user_list(request):
    users = User.objects.order_by("role", "username")
    return render(request, "accounts/user_list.html", {"users": users})


@role_required(MANAGER_ONLY)
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{user.get_role_display()} '{user.username}' created.")
            return redirect("user_list")
    else:
        form = UserCreateForm()
    return render(request, "accounts/user_form.html", {"form": form})


@role_required(MANAGER_ONLY)
@require_POST
def user_toggle_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect("user_list")
    user.is_active = not user.is_active
    user.save(update_fields=["is_active"])
    messages.success(request, f"'{user.username}' {'activated' if user.is_active else 'deactivated'}.")
    return redirect("user_list")

