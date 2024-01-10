from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Класс для создания блоговой записи
    """
    model = Blog
    fields = ('title', 'content', 'image')
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_blog'

    def form_valid(self, form):
        """
        Создаем уникальный slug
        """
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    """
    Класс для создания списка блоговых записей
    """
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        """
        Возвращает блоговые записи, которые имеют положительный признак публикации
        """
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Класс позволяет редактировать запись
    """
    model = Blog
    fields = ('title', 'content', 'image')
    template_name = 'blog/blog_form.html'
    permission_required = 'blog.change_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    template_name = 'blog/blog_confirm_delete.html'
    permission_required = 'blog.delete_blog'
