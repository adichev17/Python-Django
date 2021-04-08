from django import forms
from .models import Category, News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField



class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    сontent = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))
    captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Максимальная длина 150 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }



class NewsForm(forms.ModelForm):
    """
    title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput(attrs = {"class": "form-control"}))
    content = forms.CharField(label='Текст:', widget = forms.Textarea(attrs = {"class": "form-control", "rows": 5}))
    is_published = forms.BooleanField(label='Опубликовано?', initial=True)
    category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Категория:', queryset=Category.objects.all(), widget=forms.Select(attrs = {"class": "form-control"}))
    """
    class Meta:
        model = News
        # fields = '__all__'  #Джанго сам возьмёт все поля, но на практике так лучше не делать!
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self): # создаём собственный валидатор для title
        title = self.cleaned_data['title'] # clear data
        if re.match('\d', title): # Если начинается title с цифры
            raise ValidationError("Название не должно начинаться с цифры") # Возбуждаем исключение
        return title