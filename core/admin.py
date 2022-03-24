from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostStatement(admin.ModelAdmin):
    list_display = ('title', 'author')
