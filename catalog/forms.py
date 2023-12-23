from django import forms

from catalog.models import Product, Version
from django.forms import inlineformset_factory, BaseInlineFormSet


class ProductForm(forms.ModelForm):
    """
    Форма для валидации и стилизации продукта
    """

    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        cleaned_name = self.cleaned_data.get('name')
        words_unused = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if cleaned_name in words_unused:
            raise forms.ValidationError('Продукт запрещен к продаже на нашем сайте')

        return cleaned_name

    def clean_description(self):
        cleaned_description = self.cleaned_data.get('description')
        words_unused = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if cleaned_description in words_unused:
            raise forms.ValidationError('Описание продукта недопустимо на нашем сайте')

        return cleaned_description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VersionForm(forms.ModelForm):
    """
    Форма для версии продукта
    """

    class Meta:
        model = Version
        fields = '__all__'


VersionFormSet = inlineformset_factory(Product, Version, fields=['number_version', 'is_active_version'], extra=1)
