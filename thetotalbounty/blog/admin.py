from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from blog.models import Category, Comment, Post


class CategoryAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_on', 'is_draft']
    list_editable = ['is_draft']
    formfield_overrides = {
    models.TextField: {"widget": TinyMCE()},
}  

    def save_model(self, request, obj: Post, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)

admin.site.register(Post, PostAdmin)

admin.site.register(Comment, CommentAdmin)
