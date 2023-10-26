import graphene
from graphene_django import DjangoObjectType
from exceptions.exceptions import UnauthorizedException
from django.contrib.auth.models import User
from accounts.models import Account
from django.db.models import Subquery


class UserType(DjangoObjectType):
    image_url = graphene.String()
    class Meta:
        model = User
        fields = ("username", "image_url")

    
    def resolve_image_url(self, info):
        host_url = info.context.build_absolute_uri("/")
        return self.account.profile_image_url(host_url)


class AccountType(DjangoObjectType):
    user_info = graphene.Field(UserType)
    class Meta:
        model = Account

    def resolve_user_info(self, info):
        return self.user


class Query(graphene.ObjectType):
    common = graphene.List(AccountType, id = graphene
                                       .Int(description = "profile id which will be used to make in common users"))
    def resolve_common(self, info, id):
        if not info.context.user.is_authenticated:
            raise UnauthorizedException()
        try:
            account = Account.objects.get(id = id)
            return account.followers_list.filter(id__in = Subquery(Account.objects.get(id = info.context.user.account.id)
                                                            .followings_list.values_list("id", flat=True)))
        except Account.DoesNotExist:
            return None


schema = graphene.Schema(query = Query)
        