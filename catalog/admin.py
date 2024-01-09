from django.contrib import admin

from catalog.models import Product, Category, Contact, Version


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'number_version', 'name', 'is_active_version')
    search_fields = ('title', 'description',)


# регистрация модели контактов
admin.site.register(Contact)
