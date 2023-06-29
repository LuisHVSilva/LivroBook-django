from functools import wraps
from django.contrib.auth.decorators import login_required as original_login_required
from django.shortcuts import redirect


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')  # Redirecione o usuário para a página de login.

        return original_login_required(view_func)(request, *args, **kwargs)  # Chame a função original login_required.

    return wrapped_view
