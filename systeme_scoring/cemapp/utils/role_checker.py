from django.http import HttpResponseForbidden
from functools import wraps

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Vous devez être connecté pour accéder à cette page.")
            if user.role != required_role:
                return HttpResponseForbidden("Vous n'avez pas l'autorisation d'accéder à cette page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
