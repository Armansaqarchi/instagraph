from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from chat.models.messageModel import BaseMessage
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.db.models import Q
from accounts.exceptions.Exceptions import *
from chat.chatSerializer import ChatListSerializer
import datetime

class ChatListPaginationNumber(PageNumberPagination):
    page_size = 15


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
    this api might experience some performance issues, so it would be better to define two scenario:

    1 - use latest messages which includes this user to order the chat list correctly, and we know that by default, the messages
    get stored in database in order by sent_at date, so it would be better to get like 100 last messages
    and then order their related private chats, which this is not a good idea,
    specially when each private chat might contain so many new messages

    2- user latest message related to each private chat,
    this structure takes O(private_chats_per_page) and for any message is sent, takes O(1) to update the related chat
    """


    def get(self, request):
        account = request.user.account
        chats = account.chat_set.order_by("latest_message")
        serialized_chats = ChatListSerializer(chats, many= True)

        return Response({"data" : serialized_chats}, status=HTTP_200_OK)

        

        


    
