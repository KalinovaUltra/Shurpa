from django.core.exceptions import ValidationError
from  django.core.validators import MinLengthValidator
from django.utils.deconstruct import deconstructible
from django import forms
from .models import Category, Calorie, Shurpa


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message,code=self.code, params={"value": value})

class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категория")
    calorie = forms.ModelChoiceField(queryset=Calorie.objects.all(),empty_label="Калорийность не указана", required=False, label="Калории")
    class Meta:
        model = Shurpa
        fields = ['title', 'content', 'photo', 'is_published', 'cat', 'calorie', 'tags' ]

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) < 3:
            raise ValidationError('Длина должна быть больше 3 символов')
        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")
