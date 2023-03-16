from django.contrib import admin
from .models import Subscription
from .models import Fee
# Register your models here.
admin.site.register(Subscription)
admin.site.register(Fee)
