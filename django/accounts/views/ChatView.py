from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import datetime


class getChat(LoginRequiredMixin, APIView):
    paginate_by = 80
    login_url = settings.LOGIN_REDIRECT_URL

    def get(self, request):
        message_page = request.GET.get("message_page")
        time = datetime.datetime.today()
        time.replace(hour=0, minute=0, second=0)
        time -= datetime.timedelta(days=message_page)

        
