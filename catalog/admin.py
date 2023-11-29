from django.contrib import admin

from catalog.models import Product, Category, Contact


# Register your models here.


@admin.register(Category)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Product)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)
    search_fields = ('name', 'description',)


# регистрация модели контактов
admin.site.register(Contact)
