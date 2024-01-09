from django.db import models


class Blog(models.Model):
    """
    Модель для создания блоговой записи
    """
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.SlugField(max_length=50, verbose_name='url', blank=True, null=True)
    content = models.TextField(verbose_name='Контент')
    image = models.ImageField(upload_to='material/', verbose_name='изображение')
    create_date = models.DateTimeField(auto_now_add=True)
    publication = models.CharField(default=True, verbose_name='признак публикации')
    count = models.IntegerField(default=0, verbose_name='кол-во просмотров')

    def __str__(self):
        return f'{self.title}. {self.content}.'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блог'
        ordering = ('title',)
