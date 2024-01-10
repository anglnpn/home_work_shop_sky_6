from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Contact, Version
from catalog.forms import ProductForm, VersionFormSet

from django.db.models import OuterRef, Subquery

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin

from django.shortcuts import render


def toggle_publish(request, pk):
    """
    Функция проверяет статус публикации и присваивает противоположное значение
    """
    product_item = get_object_or_404(Product, pk=pk)
    product_item.is_published = not product_item.is_published
    product_item.save()

    return redirect(reverse('main:index'))


class ProductListView(LoginRequiredMixin, ListView):
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
                    is_active_version=True,
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

    def test_func(self):
        """
        Проверка, является ли текущий пользователь автором продукта
        """
        return self.request.user == self.get_object().author

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


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Класс для обновления данных о продукте
    """
    model = Product
    fields = ('name', 'description', 'image', 'category')
    permission_required = 'catalog.edit_published'
    success_url = reverse_lazy('main:index')
    template_name = 'main/product_update.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None
        self.request = None

    def test_func(self):

        """
        Проверка, является ли текущий пользователь автором или модератором продукта
        """
        user = self.request.user
        product_author = self.get_object().author
        return user == product_author or user.has_perm('catalog.edit_published')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['version_formset'] = VersionFormSet(self.request.POST, instance=self.object)
        else:
            data['version_formset'] = VersionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """
        Метод для установки версии продукта
        """
        context = self.get_context_data()
        version_formset = context['version_formset']

        if version_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            version_formset.instance = self.object
            version_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        """
        Переопределение метода чтобы динамически изменять поля формы
        в зависимости от принадлежности пользователя к группе "moderator".
        Если пользователь является модератором, поля 'name' и 'image' удаляются из формы.
        """
        form = super().get_form(form_class)
        user = self.request.user

        if user.groups.filter(name="moderator").exists():
            form.fields.pop('name')
            form.fields.pop('image')

        return form


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Класс для удаления продукта"""
    model = Product
    success_url = reverse_lazy('main:index')
    template_name = 'main/product_confirm_delete.html'

    def test_func(self):
        """
        Проверка, является ли текущий пользователь суперюзером
        """
        return self.request.user.is_superuser


def custom_permission_denied(request, exception):
    """
    При ошибке 403 отправляет на кастомную страницу
    """
    return render(request, 'main/403.html', status=403)
