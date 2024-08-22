from django.contrib import admin
from .models import Post, Comment, UserProfile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish']
    list_filter = ['created', 'publish', 'author']
    search_fields = ['title', 'body']
    date_hierarchy = 'publish'
    ordering = ['publish']


@admin.register(Comment) 
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created']
    list_filter = ['created', 'author']
    search_fields = ['post', 'body']
    date_hierarchy = 'created'
    ordering = ['created']
    
    
@admin.register(UserProfile) 
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'date_of_birth']
    list_filter = ['date_of_birth', 'user']
    search_fields = ['user', 'date_of_birth']
    date_hierarchy = 'date_of_birth'
    ordering = ['date_of_birth']
    