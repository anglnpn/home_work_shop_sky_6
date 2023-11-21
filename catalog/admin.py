from django.contrib import admin

from catalog.models import Product, Category, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Регистрация модели категорий товаров в админке
    """
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
       Регистрация модели продуктов в админке
       """
    list_display = ('name', 'description',)
    search_fields = ('name', 'description',)


# регистрация модели контактов
admin.site.register(Contact)
