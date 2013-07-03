from django.contrib.auth.decorators import user_passes_test

from django_otp import devices_for_user
from django_otp.conf import settings


def otp_required(view=None, redirect_field_name='next', login_url=None, if_configured=False):
    """
    Similar to :func:`~django.contrib.auth.decorators.login_required`, but
    requires the user to be :term:`verified`. By default, this redirects users
    to :setting:`OTP_LOGIN_URL`.

    :param if_configured: If ``True``, an authenticated user with no confirmed
        OTP devices will be allowed. Default is ``False``.
    :type if_configured: bool
    """
    if login_url is None:
        login_url = settings.OTP_LOGIN_URL

    if if_configured:
        def test(user):
            try:
                if user.is_authenticated():
                    next(devices_for_user(user, confirmed=True))
            except StopIteration:
                return True  # No devices
            else:
                return user.is_verified()
    else:
        test = lambda u: u.is_verified()

    decorator = user_passes_test(test, login_url=login_url, redirect_field_name=redirect_field_name)

    return decorator if (view is None) else decorator(view)
