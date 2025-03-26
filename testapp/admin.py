from django.contrib import admin

# Register your models here.
from testapp.models import *
admin.site.register(Task)
admin.site.register(CustomUser)