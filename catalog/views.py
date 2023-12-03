from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Contact, Blog


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'main/index.html'


# def index(request):
#     # Выборка последних 5 товаров
#     latest_products = Product.objects.all()
#
#     context = {
#         'object_list': latest_products
#     }
#
#     return render(request, 'main/index.html', context)

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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/product.html'


# def show_product(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     data = {'title': f'Страница с описанием продукта{product.name}', 'product': product}
#     return render(request, 'main/product.html', context=data)

class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'image')
    template_name = 'main/blog_form.html'
    success_url = reverse_lazy('main:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    template_name = 'main/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'main/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'image')
    template_name = 'main/blog_form.html'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('main:list')
    template_name = 'main/blog_confirm_delete.html'
