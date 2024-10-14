from django.contrib import admin
from blog.models import Category, Comment, Post


class CategoryAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_draft']
    list_editable = ['is_draft']


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)

admin.site.register(Post, PostAdmin)

admin.site.register(Comment, CommentAdmin)
