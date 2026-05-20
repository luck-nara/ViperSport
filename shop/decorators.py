from functools import wraps

from django.conf import settings
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_viper_admin'):
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)

    return wrapper


def verify_admin(username, password):
    return (
        username == settings.ADMIN_USERNAME
        and password == settings.ADMIN_PASSWORD
    )
