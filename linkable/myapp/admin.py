from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from .models import Book,Recommend

admin.site.register(Book)
admin.site.register(MyUser)
admin.site.register(Recommend)