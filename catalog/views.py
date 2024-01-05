from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Contact, Blog, Version
from catalog.forms import ProductForm, VersionFormSet

from django.db.models import OuterRef, Subquery

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class ProductListView(ListView):
    """
    Класс для создания списка продуктов
    """
    model = Product
    template_name = 'main/index.html'

    def get_queryset(self):
        """
        Возвращает активную версию продукта для отображения в карточке продукта
        """
        return Product.objects.annotate(
            active_version_number=Subquery(
                Version.objects.filter(
                    product=OuterRef('pk'),
                    is_active_version=True
                ).values('number_version')[:1]
            )
        )


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


class ProductDetailView(DetailView):
    """
    класс для выведения информации о продукте
    """
    model = Product
    template_name = 'main/product.html'


class BlogCreateView(CreateView):
    """
    Класс для создания блоговой записи
    """
    model = Blog
    fields = ('title', 'content', 'image')
    template_name = 'main/blog_form.html'
    success_url = reverse_lazy('main:list')

    def form_valid(self, form):
        """
        Создаем уникальный slug
        """
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """
    Класс для создания списка блоговых записей
    """
    model = Blog
    template_name = 'main/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Возвращает блоговые записи, которые имеют положительный признак публикации
        """
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
    """
    Класс позволяет редактировать запись
    """
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания продукта
    """
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('main:index')
    template_name = 'main/new_product_form.html'

    def __init__(self):
        self.request = None
        self.object = None

    def get_context_data(self, **kwargs):
        """
        Получаем список версий продукта из формсета
        """
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['version_formset'] = VersionFormSet(self.request.POST)
        else:
            data['version_formset'] = VersionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        version_formset = context['version_formset']
        if version_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user  # Установка автора продукта
            self.object.save()
            version_formset.instance = self.object
            version_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для обновления данных о продукте
    """
    model = Product
    fields = ('name', 'description', 'image')
    success_url = reverse_lazy('main:index')
    template_name = 'main/new_product_form.html'

    def __init__(self):
        self.object = None
        self.request = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['version_formset'] = VersionFormSet(self.request.POST, instance=self.object)
        else:
            data['version_formset'] = VersionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """
        Форма для установки версии продукта
        """
        context = self.get_context_data()
        version_formset = context['version_formset']
        if version_formset.is_valid():
            self.object = form.save()
            self.object.author = self.request.user
            version_formset.instance = self.object
            version_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('main:index')
    template_name = 'main/product_confirm_delete.html'

