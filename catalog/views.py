from django.shortcuts import render
from catalog.models import Product, Contact


# Create your views here.

def index(request):
    # Выборка последних 5 товаров
    latest_products = Product.objects.order_by('-create_date')[:5]
    # Вывод данных в консоль
    for product in latest_products:
        print(f"Product: {product.name}, Description: {product.description}")

    return render(request, 'main/index.html')


def contacts(request):
    """
    Функция получает данные, введенные пользователем
    """
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     phone = request.POST.get('phone')
    #     message = request.POST.get('message')
    #     print(f'{name} {phone}: {message}')

    contacts_ = Contact.objects.all()
    return render(request, 'main/contacts.html', {'contacts': contacts_})


def categories(request):
    return render(request, 'main/categories.html')
