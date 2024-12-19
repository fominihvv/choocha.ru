from django import forms
# from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Note


@deconstructible
class RussianValidator:
    ALLOWED_CHARACTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать только русские буквы, цифры, дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARACTERS)):
            raise forms.ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана")

    class Meta:
        model = Note
        fields = ['title', 'content', 'image', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        # validators = {
        #    'title': RussianValidator(),
        # }
        # labels = {
        #    'title': 'Заголовок',
        # }

    # def clean_title(self):
    #     allowed_characters = "абвгдеёжзий̆клмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ123456789- "
    #     title = self.cleaned_data['title']
    #     if not set(title).issubset(set(allowed_characters)):
    #         raise forms.ValidationError('Должны присутствовать только русские буквы, цифры, дефис и пробел. V2')
    #     return title



class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")
