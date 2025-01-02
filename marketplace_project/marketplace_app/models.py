from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

# Модель для пользователя (клиента или мастера)
class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    USER_TYPE_CHOICES = (
        ('client', _('Client')),  # Роль клиента
        ('master', _('Master')),  # Роль мастера
    )

    user_type = models.CharField(max_length=6, choices=USER_TYPE_CHOICES, default='client')

    def __str__(self):
        return self.username

# Модель для продукта
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Поле для изображения

    def __str__(self):
        return self.name

# Модель для мастера
class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='master_profile')
    description = models.TextField(blank=True)
    portfolio = models.ImageField(upload_to='masters/portfolio/', blank=True, null=True)  # Портфолио мастера
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    available_times = models.JSONField()  # Список доступных времён для записи

    def __str__(self):
        return f"Profile of {self.user.username}"

# Модель для отзыва
class Review(models.Model):
    master = models.ForeignKey(Master, related_name='reviews', on_delete=models.CASCADE)
    client = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()  # Рейтинг от 1 до 5
    comment = models.TextField()  # Комментарий

    def __str__(self):
        return f"Review by {self.client.username} for {self.master.user.username}"

# Модель для заказа
class Order(models.Model):
    client = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    master = models.ForeignKey(Master, related_name='orders', on_delete=models.CASCADE)
    time = models.DateTimeField()  # Время бронирования
    status = models.CharField(max_length=10, default='pending')  # Статус заказа (например, ожидает подтверждения)

    def __str__(self):
        return f"Order by {self.client.username} for {self.master.user.username}"
