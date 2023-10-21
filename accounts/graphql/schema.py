import graphene
from graphene_django import DjangoObjectType
from exceptions.exceptions import NotFoundException, UnauthorizedException
from accounts.models import Account
from utils.common import TokenMiddleware
from django.db.models import Subquery


class AccountType(DjangoObjectType):
    class Meta:
        model = Account
        fields = ("id", "user", "is_private")

class Query(graphene.ObjectType):
    common = graphene.List(AccountType, id = graphene
                                       .Int(description = "profile id which will be used to make in common users"))

    def resolve_common(self, info, id):
        if not info.context.user.is_authenticated:
            raise UnauthorizedException()
        try:
            account = Account.objects.get(id = id)
            return account.followers_list.filter(id__in = Subquery(Account.objects.get(info.context.user.account.id)
                                                            .followings_list.values_list("id", flat=True)))
        except Account.DoesNotExist:
            raise NotFoundException("account object not found")


schema = graphene.Schema(query = Query)
        