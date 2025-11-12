from django.contrib import admin
from posts.models import Post
from django.contrib import admin
from posts.models import Section, Category, Post
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


admin.site.register(Section, admin.ModelAdmin)


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    list_display = ['name', 'full_path']

    form = movenodeform_factory(Category)


admin.site.register(Post, admin.ModelAdmin)
