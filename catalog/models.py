from datetime import timezone

from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """
    Модель для продуктов
    """
    name = models.CharField(max_length=50, verbose_name='название')
    description = models.CharField(max_length=200, verbose_name='описание')
    image = models.ImageField(upload_to='product/', verbose_name='изображение', **NULLABLE)
    category = models.CharField(max_length=50, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена за покупку')
    create_date = models.DateTimeField(verbose_name='дата создания')
    edit_date = models.DateTimeField(verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)


class Category(models.Model):
    """
    Модель для категорий
    """
    name = models.CharField(max_length=50, verbose_name='название')
    description = models.CharField(max_length=200, verbose_name='описание')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Contact(models.Model):
    """
    Модель для контактов
    """
    name = models.CharField(max_length=50, verbose_name='название организации')
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return f'{self.name}. {self.email}. {self.phone_number}. {self.address}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ('name',)
