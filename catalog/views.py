from django.shortcuts import render
from catalog.models import Product, Contact


# Create your views here.

def index(request):
    # Выборка последних 5 товаров
    product_list = Product.objects.all()

    context = {
        'object_list': product_list,
        'title': 'Главная'
    }
    # Вывод данных в консоль
    # for product in latest_products:
    #     print(f"Product: {product.name}, Description: {product.description}")

    return render(request, 'main/index.html', context)


def contacts(request):
    """
    Функция получает данные, введенные пользователем
    """
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     phone = request.POST.get('phone')
    #     message = request.POST.get('message')
    #     print(f'{name} {phone}: {message}')

    context = {
        'title': 'Контакты'
    }

    contacts_ = Contact.objects.all()
    return render(request, 'main/contacts.html', {'contacts': contacts_})


def categories(request):
    context = {
        'title': 'Категории'
    }
    return render(request, 'main/categories.html', context)


def product(request):
    product_list = Product.objects.all()

    context = {
        'object_list': product_list,
        'title': 'Товар'
    }
    return render(request, 'main/product.html', context)
