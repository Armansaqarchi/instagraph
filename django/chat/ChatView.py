from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from accounts.models import BaseMessage
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.db.models import Q
from accounts.exceptions.Exceptions import *
import datetime


class getChat(LoginRequiredMixin, APIView):
    paginate_by = 80
    login_url = settings.LOGIN_REDIRECT_URL

    def get(self, request):
        try:
            message_page = request.GET.get("message_page")
            recipient = request.GET.get("recipient")
            time = datetime.datetime.today().date()
            time = time - datetime.timedelta(days=message_page)

            query = (Q(sent_at__date__gt = time) & Q(sent_at__date__lt = time + datetime.timedelta(days = 1)) & 
            Q(sender = request.user.account) & Q(recipient = recipient))

            BaseMessage.objects.filter(query)
            return Response({"message": "success", "status" : "success"}, status=HTTP_200_OK)
        except KeyError as e:
            BadRequestException(str(e))
        
