from django.contrib import admin
from products.models import Platform, Category, Product, Link
from treebeard.forms import movenodeform_factory
from treebeard.admin import TreeAdmin

admin.site.register(Platform, admin.ModelAdmin)


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Link, admin.ModelAdmin)
