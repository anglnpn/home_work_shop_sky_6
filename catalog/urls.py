from django.urls import path

from catalog.apps import MainConfig
from catalog.views import contacts, categories, ProductListView, ProductDetailView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, toggle_publish

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('categories/', categories, name='categories'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete_product/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
    path('toggle/<int:pk>/', toggle_publish, name='toggle'),

]
