from rest_framework.viewsets import ModelViewSet
from ..permissions import isFollowerOrPublicPermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from accounts.permissions import IsOwnerPermission
from accounts.models import Account
from posts.models import Post
from exceptions.exceptions import *
from ..models import Like, Comment
from ..serializer.Homeserializer import LikesSerializer, CommentSerializer

class PostViewAPI(ModelViewSet):
    """
    Post API View
    user can create post using post:create
    user can partial_update using patch :: partial update
    user can destroy the post using delete :: destroy
    """

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


class LikeAPIView(ModelViewSet):
    """
    Like API view:
    user likes posts using get :: retreive method
    user dislikes (removes) the like using delete :: destroy
    user sees post likes using get :: list
    """

    pagination_class = "# must complete"
    queryset = Post.objects.all()


    PERMISSION_CASES = {
        "get" : isFollowerOrPublicPermission,
        "delete" : IsOwnerPermission
    }

    def get_like(self, pk):
        try:
            return Like.objects.get(pk = pk)
        except Like.DoesNotExist:
            raise NotFoundException("No such Like object", code = "object_not_found")

    def get_permissions(self):
        return self.PERMISSION_CASES[self.request.method.lower()]

    def retrieve(self, request, pk, *args, **kwargs):
        post = self.get_object()
        like = Like.objects.create(
            user = self.request.user.account,
            post = post
        )
        return Response({"data" : like, "Message" : "post liked", "Status" : "Success", "Code" : "liked"}, status= HTTP_200_OK)
        

    def list(self, request, pk, *args, **kwargs):
        post = self.get_object()
        likes = LikesSerializer(instance= post.likes, many = True, context = {"account" : self.request.user.account})
        return Response({"data" : likes.data, "Message" : f"likes for post {post.id}", "Status" : "Success", "Code" : "post_likes"}, status=HTTP_200_OK)
        
    
    def destroy(self, request, pk, *args, **kwargs):
        like = self.get_like(pk = pk)
        like.delete()
        return Response({"Message" : "like object deleted", "Status" : "Success", "Code" : "like_deleted"}, status=HTTP_204_NO_CONTENT)

