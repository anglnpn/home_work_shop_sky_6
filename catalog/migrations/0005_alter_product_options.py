# Generated by Django 4.2.8 on 2024-01-09 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_is_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('name',), 'permissions': [('set_published', 'Can publish posts')], 'verbose_name': 'продукт', 'verbose_name_plural': 'продукты'},
        ),
    ]
