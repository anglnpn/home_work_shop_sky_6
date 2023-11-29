from django.urls import path

from catalog.views import index, contacts, categories

urlpatterns = [
    path('', index,  name='index'),
    path('contacts/', contacts,  name='contacts'),
    path('categories/', categories,  name='categories'),
    path('product/', categories,  name='product')
]
