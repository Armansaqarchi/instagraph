from rest_framework.viewsets import ModelViewSet
from ..permissions import IsFollowerOrPublicPermission
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_206_PARTIAL_CONTENT,
    HTTP_201_CREATED
)
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
        "get" : IsFollowerOrPublicPermission,
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
        "get" : IsFollowerOrPublicPermission,
        "delete" : IsOwnerPermission,
    }

    def get_like(self, pk):
        try:
            like = Like.objects.get(pk = pk)
        except Like.DoesNotExist:
            raise NotFoundException("No such Like object", code = "object_not_found")
        self.check_object_permissions(request=self.request, obj = like.user)
        return like

    def get_permissions(self):
        return [self.PERMISSION_CASES[self.request.method.lower()]()]

    def create(self, request, pk, *args, **kwargs):
        post = self.get_object()
        account = request.user.account
        serialized_like = LikesSerializer(data = {"user" : account.id, "post" : post.id},
                                           context = {"account" : request.user.account})
        try:
            serialized_like.is_valid(raise_exception=True)
        except ValidationError as e:
            raise BadRequestException("invalid request data type", code = "bad_like_request")
        
        serialized_like.save()

        return Response({"data" : serialized_like.data, "Message" : "post liked", "Status" : "Success", "Code" : "liked"}, status= HTTP_201_CREATED)
    

    def retrieve(self, request, pk, *args, **kwargs):
        like = self.get_like(pk = pk)
        data = LikesSerializer(instance = like).data
        return Response({"data" : data, "Message" : "the like details are provided", "Code" : "like_retreive", "Status" : "Success"},
                        status=HTTP_200_OK)
        

    def list(self, request, pk, *args, **kwargs):
        post = self.get_object()
        likes = LikesSerializer(instance= post.likes, many = True, context = {"account" : self.request.user.account})
        return Response({"data" : likes.data, "Message" : f"likes for post {post.id}", "Status" : "Success", "Code" : "post_likes"}, status=HTTP_200_OK)
        
    
    def destroy(self, request, pk, *args, **kwargs):
        like = self.get_like(pk = pk)
        like.delete()
        return Response({"Message" : "like object deleted", "Status" : "Success", "Code" : "like_deleted"}, status=HTTP_204_NO_CONTENT)


class CommentAPIView(ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    PERMISSION_CASES = {
        "delete" : IsOwnerPermission,
        "get" : IsFollowerOrPublicPermission,
        "patch" : IsOwnerPermission,
        "post" : IsFollowerOrPublicPermission
    }

    def get_permissions(self):
        return [self.PERMISSION_CASES[self.request.method.lower()]()]
    

    def get_object(self, pk, model, check_object = ""):
        """
        kind of overridden method for get_object that is more customized
        by default, check_object_permission is performed on the same target object.
        but sometimes needed to be checked for at attribute associated with that object
        
        @param:
            model : the model to make db query for
            check_object : the attribute associated with that object that might be consider as the permission check target
        """
        try:
            instance = model.objects.get(pk = pk)
        except model.DoesNotExist:
            raise NotFoundException("No such post", code = "post_id_invalid")
        check_object = getattr(instance, check_object, None) or instance
        self.check_object_permissions(request = self.request, obj = check_object)
        return instance
 

    def create(self, request, pk, *args, **kwargs):
        comment = request.data["content"]
        post = self.get_object(pk=pk, model = Post, check_object="user")
        Comment.objects.create(
            user = request.user.account,
            content = comment,
            post = post
        )
        return Response({"Message" : "comment successfully created", "Status" : "Success", "Code" : "post_comment"},
                         status=HTTP_201_CREATED)
        
    
    def list(self, request, pk, *args, **kwargs):
        post = self.get_object(pk=pk, model = Post)
        comments = post.post_comments
        serialized_comments = self.serializer_class(instance= comments, many = True)
        return Response({"data" : serialized_comments.data, "Messages" : f"post {post.id} comments are provided", "Status" : "Success", "Code" : "comments_list"},
                         status=HTTP_200_OK)
    
    
    def destroy(self, request, pk, *args, **kwargs):
        comment = self.get_object(pk = pk, model = Comment, check_object="user")
        comment.delete()
        return Response({"Message" : "comment successfully deleted", "Code" : "comment_deleted", "Status" : "Success"}, status=HTTP_204_NO_CONTENT)
    
    def retrieve(self, request, pk, *args, **kwargs):
        comment = self.get_object(pk = pk, model = Comment, check_object="post")
        comment_data = self.serializer_class(instance = comment).data
        return Response({"data" : comment_data, "Message" : "here is the comment",
                          "Status" : "Success", "Code" : "comment_provided"}, status=HTTP_200_OK)
    
    def partial_update(self, request, pk, *args, **kwargs):
        updated_data = request.data
        comment = self.get_object(pk = pk, model = Comment)
        new_data = self.serializer_class(instance= comment, data = updated_data, partial = True)
        new_data.is_valid(raise_exception= True)
        new_data.save()
        return Response({"data" : new_data.data, "Message" : "comment successfully updated", "Code" : "comment_updated", "Status" : "Success"}, 
                        status=HTTP_206_PARTIAL_CONTENT)