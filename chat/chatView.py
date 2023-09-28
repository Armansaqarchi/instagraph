from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from chat.models.messageModel import BaseMessage
from rest_framework.response import Response
from django.views import View
from rest_framework.status import HTTP_200_OK
from .chatSerializer import *
from django.shortcuts import render
from django.db.models import Q
from exceptions.exceptions import *
from rest_framework.generics import GenericAPIView
from chat.models.chatModel import Chat
import datetime

class ChatListPaginationNumber(PageNumberPagination):
    page_size = 15

class GetMessages(APIView):
    paginate_by = 80

    def get(self, request, pk):
        """
        used to get messages and paginating them for better performance
        """
        try:
            message_page = int(request.GET.get("page"))
            time = datetime.datetime.today().date()
            time = time - datetime.timedelta(days=message_page)

            query = (Q(sent_at__date__gte = time) & Q(sent_at__date__lt = time + datetime.timedelta(days = 1)) & 
            Q(chat = pk))

            messages = BaseMessage.objects.filter(query)
            serialized_messages = ChatMessageSerializer(instance=messages)
            return Response({"data" : serialized_messages.data, "Message": "success", "Status" : "success", "Code" : "messages_list"}, status=HTTP_200_OK)
        except KeyError as e:
            BadRequestException(str(e))
        except ValueError:
            raise BadRequestException("page query parameter must be of type int", code = "value_format_error")
        
class ChatView(APIView):
    def get(self, requset):
        return render(request=requset, template_name="test_ws.html")

        
class GetChatList(GenericAPIView):
    """
    this api might experience some performance issues, so it would be better to define two scenarios:

    1 - use latest messages which includes this user to order the chat list correctly, and we know that by default, the messages
    are stored ordered by sent_at date, so it would be better to get like 100 last messages
    and then order their related private chats, which this is not a good idea,
    specially when each private chat might contain so many new messages

    2- user latest message related to each private chat,
    this structure takes O(private_chats_per_page) and for any message is sent, takes O(1) to update the related chat
    """

    class ChatListpagination(PageNumberPagination):
        page_query_param = "page"
        page_size = 20
        max_page_size = 30

    pagination_class = ChatListpagination

    def get_chats(self, account):
        return account.chat_set.annotate(messages__last)

    def get(self, request):
        account = request.user.account
        chats = account.chat_set.order_by("latest_message")
        paged_chat = self.paginate_queryset(chats)

        serialized_chats = ChatMessageSerializer(paged_chat, many= True)

        return Response({"data" : serialized_chats.data}, status=HTTP_200_OK)

        

        


    
