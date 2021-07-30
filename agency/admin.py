from django.contrib import admin
from django.contrib.admin.options import HORIZONTAL
from .models import House,  Profile


# Register your models here.
admin.site.register(House)
admin.site.register(Profile)



