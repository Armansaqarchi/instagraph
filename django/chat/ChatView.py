from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from accounts.models import BaseMessage
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.db.models import Q
from accounts.exceptions.Exceptions import *
import datetime


class GetMessages(APIView):
    paginate_by = 80

    def get(self, request):
        """
        used to get messages and paginating them for better performance
        """
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
        
class getChatList(APIView):
    """
    this api uses aggregation to get the chats based on last messages sent in them
    SELECT recipient, max(sent_at) as latest_message FROM base_message GROUP BY recipient ORDER BY latest_message
    """
    paginate_by = 30


    def get(self, request):
        account = request.user.account
        

    
