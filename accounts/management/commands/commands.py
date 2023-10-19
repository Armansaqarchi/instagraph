from django.core.management.base import BaseCommand, CommandParser
from accounts.models import Account
from posts.models import Post
from django.db.models import OuterRef, Subquery
from django.db.models import Count, Case, When, F, Q, DateTimeField
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Displays current time'


    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--top-users", nargs="*", help="queries for top 100 users based on their followers number")
        parser.add_argument("--inactive-users", nargs="*", help="queries for top inactive users based on their recent activities")
        parser.add_argument("--active-users", nargs="*", help="queries for active users")

    def handle(self, *args, **options):
        print(options)
        if options.get("top_users", None) != None:
            self.handle_top_users()
        if options.get("inactive_users") != None:
            self.handle_top_inactive_users()
        if options.get("active_users") != None:
            self.handle_active_users()


    def handle_top_users(self):
        limit = max(100, Account.objects.count())
        queryset = Account.objects.all().order_by("-followers")[:limit]
        self.stdout.write(self.style.SUCCESS("HERE ARE THE TOP USERS:\n\n\n"))
        for i in queryset:
            username = "{: <50}".format(i.user.username)
            followers = "{: <15}".format(i.followers)
            self.stdout.write(self.style.SUCCESS(f"{username}{followers}"))

    def handle_top_inactive_users(self):
        last_post_subquery = Post.objects.filter(user = OuterRef("id")).order_by("-created_at").values("created_at")[:1]
        queryset = Account.objects.all().annotate(last_activity = Case(When(
            user__last_login__gt = last_post_subquery, then=F("user__last_login")),
              default=last_post_subquery, output_field=DateTimeField())) \
            .order_by("last_activity")
        
        self.stdout.write(self.style.SUCCESS("HERE ARE THE LIST OF INACTIVE USERS"))
        no = 0
        for i in queryset:
            no += 1
            username = "{: <50}".format(i.user.username)
            user_no = "{: <4}".format(no)
            self.stdout.write(self.style.SUCCESS(f"{user_no}{username}"))


    def handle_active_users(self):
        last_month_date = datetime.now() - timedelta(days=30)
        recent_post_subquery = Subquery(Post.objects.filter(user = OuterRef("id")).filter(created_at__gt = last_month_date).values("id"))
        queryset = Account.objects.annotate(recent_posts = Count(recent_post_subquery)).filter(recent_posts__gt = 5)
        no = 0
        for i in queryset:
            no += 1
            username = "{: <50}".format(i.user.username)
            user_no = "{: <4}".format(no)
            self.stdout.write(self.style.SUCCESS(f"{user_no}{username}"))
