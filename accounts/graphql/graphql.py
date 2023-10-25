from graphene_django.views import GraphQLView
from utils.common import TokenMiddleware
from exceptions.exceptions import UnauthorizedException, BadRequestException
from accounts.models import Account

class GraphAuthorizedView(GraphQLView):
    """
    a more secured view for graphql end points.
    by defualt, GraphQLView class does not handle the authorization of a request.
    this class authorizes the user for further usages.
    """


    def dispatch(self, request, *args, **kwargs):
        user_id = TokenMiddleware.verify_token(request.META)
        if not user_id:
            raise UnauthorizedException("unable to authoriza user")
        
        try:
            account = Account.objects.get(id = user_id)
        except Account.DoesNotExist:
            raise BadRequestException("invalid user credentials")
        

        request.user = account.user
        return super().dispatch(request, *args, **kwargs)