from rest_framework.viewsets import ModelViewSet
from ..permissions import isFollowerOrPublicPermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from accounts.permissions import IsOwnerPermission
from accounts.models import Account
from posts.models import Post
from posts.serializer.Homeserializer import PostSerializer

class PostViewAPI(ModelViewSet):

    class PostPagination(PageNumberPagination):
        page_query_param = "page"
        max_page_size = 20
        page_size = 9

    
    pagination_class = PostPagination
    serializer_class = Post

    PERMISSION_CASES = {
        "get" : isFollowerOrPublicPermission,
        "patch" : IsOwnerPermission
    }

    def get_queryset(self):
        method = self.request.method.lower()
        if method == "patch":
            self.model = Post
        else:
            self.model =  Account
        return self.model.objects.all()

    def get_permissions(self):
        return self.PERMISSION_CASES[self.request.method.lower()]
    

    def create(self, request, *args, **kwargs):
        response = super().create(request=request, *args, **kwargs)
        response.data = {"data" : response.data, "Message" : "post successfully created", "Status" : "success", "Code" : "post_created"}

    def list(self, request, pk):
        account = self.get_object()
        posts = account.posts_list
        page_posts = self.paginate_queryset(posts)
        page_posts_serialized = self.serializer_class(page_posts, many = True).data

        return Response({"data" : page_posts_serialized, "Message" : "posts are ready to show", "Code" : "posts_fetched", "Status" : "success"},
                        status=HTTP_200_OK)
    

    def partial_update(self, request, pk):
        response = super().partial_update()
        response.data = {"data" : response.data, "Message" : "the post successfully edited", "Code" : "post_edited", "Status" : "Success"}
        return response
    

    def destroy(self, request, pk):
        response = super().destroy()
        response.data = {"Message" : "post successfully deleted", "Code" : "message_deleted", "Status" : "success"}
        return response


        