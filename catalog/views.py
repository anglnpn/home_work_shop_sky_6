from django.shortcuts import render, get_object_or_404

from catalog.models import Product, Contact


# Create your views here.

def index(request):
    # Выборка последних 5 товаров
    latest_products = Product.objects.all()

    context = {
        'object_list': latest_products
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

    contacts_ = Contact.objects.all()
    return render(request, 'main/contacts.html', {'contacts': contacts_})


def categories(request):
    return render(request, 'main/categories.html')


# Product.objects.category_set
# Product.objects.category


def show_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    data = {'title': f'Страница с описанием продукта{product.name}', 'product': product}
    return render(request, 'main/product.html', context=data)

# def show_product(request, pk):
#     product = {
#         'object': Product.objects.get(pk=pk),
#         'title': 'Товары'
#     }
#     return render(request, 'main/product.html', product)
