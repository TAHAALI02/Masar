from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import User

BOTH = (User.Role.FLEET_MANAGER, User.Role.DISPATCHER)
MANAGER_ONLY = (User.Role.FLEET_MANAGER,)


def role_required(allowed_roles):
    """Anonymous -> login page. Logged in with the wrong role -> 403."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator