from django.contrib import admin
from .models import Story, Account, Follows
# Register your models here.



admin.site.register(Story)
admin.site.register(Account)
admin.site.register(Follows)