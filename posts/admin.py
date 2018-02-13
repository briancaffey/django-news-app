from django.contrib import admin
from .models import Post, LastUpdate
# Register your models here.

admin.site.register(Post)

admin.site.register(LastUpdate)