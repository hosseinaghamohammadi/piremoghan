from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Person, Article
# Register your models here.

admin.site.register(Person)
admin.site.register(Article)

