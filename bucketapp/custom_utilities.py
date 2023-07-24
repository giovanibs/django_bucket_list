from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME

# ------------------------------------------------------------------------------
# HELPER FUNCS/CLASSES
# ------------------------------------------------------------------------------

def login_required_or_anonymous(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in or is
    Anonymous, redirecting to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated or u.is_anonymous,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

class LoginRequiredOrAnonymousMixin(AccessMixin):
    """Verify that the current user is authenticated or
    is an Anonymous user."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_anonymous:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)