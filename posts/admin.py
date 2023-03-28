from django.contrib import admin
from .models import Account, Follows
# Register your models here.



admin.site.register(Follows)
admin.site.register(Account)