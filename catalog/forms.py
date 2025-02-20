from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Tool

class OrderForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ваше имя")
    email = forms.EmailField(label="Email")
    phone = forms.CharField(max_length=15, label="Телефон")
    address = forms.CharField(widget=forms.Textarea, label="Адрес доставки")

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Электронная почта", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Обязательное поле. Только буквы, цифры и @/./+/-/_'
        self.fields['password1'].help_text = 'Пароль должен содержать минимум 8 символов и не быть слишком простым.'
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения.'

class CustomLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']
        labels = {
            'username': 'Имя пользователя',
            'password': 'Пароль',
        }

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'description', 'price', 'stock', 'image', 'category', 'is_popular']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'stock': 'Количество на складе',
            'image': 'Изображение',
            'category': 'Категория',
            'is_popular': 'Популярный товар',
        }