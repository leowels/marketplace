from django import forms
from .models import User, Master, Order, Review, Product
from django.contrib.auth.forms import UserCreationForm


# Форма регистрации пользователя
class UserRegistrationForm(UserCreationForm):
    # Дополнительные поля для регистрации пользователя (например, телефон и email)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']  # Изменены имена полей для пароля
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

# Форма регистрации мастера
class MasterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ['description', 'portfolio', 'price', 'available_times']

# Форма для создания заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['time']

# Форма для отзыва
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

# Форма для добавления продукта
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']  # Пример полей для продукта
