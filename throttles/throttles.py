from rest_framework.throttling import SimpleRateThrottle
from django.contrib.auth.models import User
from django.conf import settings

class LoginThrottle(SimpleRateThrottle):
    """
    overwritten class for SimpleRateThrottle.
    by default, when user tries to log in, they are limited to send requests.
    so they will be suspended for a short time and unable to make any actions to the server.
    this is where recaptcha comes to the rescue, captcha provides a challange in order to verify 
    whether user is not a bot.
    the following use a method called 'g_response_token'.


    @how it works?
        the widget which is in charge to provide a challange for the user generates a token after a successfull attempt.
        then, sends it to the server for validation.
        after the the token is received, the server could validate the token by sending post request
        to the google recaptcha verification server.
        on a successfull action, the google returns a json response having an attribute 'success', indicating if the token is valid.
    """
    scope = "LoginAttemptRate"

    def get_cache_key(self, request, view):
        try:
            user = User.objects.get(request.data.get("email"))
        except User.DoesNotExist:
            user = None
        ident = user.pk if user else self.get_ident()
        return self.cache_format % {
            "scope" : self.scope,
            "ident" : ident
        }

    def allow_request(self, request, view):
        allow = super().allow_request(request, view)
        if allow:
            return True
        if self.check_captcha(request=request):
            return True
        return False
    
    @staticmethod
    def verify_captcha(g_value):
        credentials = {
            "response" : g_value,
            "secret" : settings.GOOGLE_RECAPTCHA_SECRET
        }
        

    def check_captcha(self, request):
        g_value = self.request.data.get("recaptcha")
        if g_value:
            return self.verify_captcha(g_value)
        return False