from django.conf  import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def anonymous_required(function=None, redirect_url=None):
   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator


def admin_only(function):
   def _inner(request, *args, **kwargs):
       if not request.user.is_admin:
           raise PermissionDenied           
       return function(request, *args, **kwargs)
   return _inner
