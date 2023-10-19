from django.core.management.base import BaseCommand, CommandParser
from accounts.models import Account
from posts.models import Post
from django.db.models import OuterRef, Subquery
from django.db.models import Min, Max
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Displays current time'


    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--top-users", help="queries for top 100 users based on their followers number")
        parser.add_argument("--inactive-users", help="queries for top inactive users based on their recent activities")
        parser.add_argument("--active-users", help="queries for active users")

    def handle(self, *args, **options):
        if options.get("top-users", None):
            self.handle_top_users()
        if options.get("inactive-users"):
            self.handle_active_users()
        if options.get("active-users"):
            self.handle_active_users()


    def handle_top_users(self):
        limit = max(100, Account.objects.count())
        queryset = Account.objects.all().order_by("-followers")[:limit]
        self.stdout(self.style.SUCCESS("HERE ARE THE TOP USERS:\n\n\n"))
        for i in queryset:
            username = "{: >50}".format(i.user.username)
            followers = "{: >15}".format(i.followers)
            self.stdout(self.style.SUCCESS(f"{username}{followers}"))

    def handle_top_inactive_users(self):
        last_post_subquery = Post.objects.filter(user = OuterRef("id")).order_by("-create_at").first().created_at
        queryset = Account.objects.all().annotate(last_activity = Max(Subquery(last_post_subquery), "user__last_login")) \
            .order_by("last_activity")
        self.stdout(self.style.SUCCESS("HERE ARE THE LIST OF INACTIVE USERS"))
        no = 0
        for i in queryset:
            no += 1
            username = "{: >50}".format(i.user.username)
            user_no = "{: >4}".format(no)
            self.stdout(self.style.SUCCESS(f"{user_no}{username}"))


    def handle_active_users(self):
        last_month_date = datetime.now() - timedelta(days=30)
        recent_post_subquery = Post.objects.filter(user = OuterRef("id")).filter(created_at__gt = last_month_date).count()
        queryset = Account.objects.annotate(recent_posts = Subquery(recent_post_subquery)).filter(recent_post__gt = 5)
        no = 0
        for i in queryset:
            no += 1
            username = "{: >50}".format(i.user.username)
            user_no = "{: >4}".format(no)
            self.stdout(self.style.SUCCESS(f"{user_no}{username}"))
