from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Master, Product, Order, Review  # добавьте модели, если нужно
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


# Кастомная форма регистрации пользователя
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Форма добавления продукта
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']  # Пример полей для продукта

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

# Форма регистрации мастера
class MasterRegistrationForm(forms.ModelForm):
    class Meta:
        model = Master
        fields = ['description', 'portfolio', 'price', 'available_times']

def home(request):
    return render(request, 'home.html')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Перенаправление на страницу списка продуктов
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Авторизация после регистрации
            return redirect('home')  # Перенаправление на главную страницу после регистрации
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

# Авторизация пользователя
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Авторизация пользователя
            return redirect('home')  # Перенаправление на главную страницу после входа
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')  # Отображение формы логина

def logout_view(request):
    logout(request)  # Выход из системы
    return redirect('login')  # Перенаправление на страницу входа после выхода

# Список продуктов
def product_list(request):
    products = Product.objects.all()  # Получение всех продуктов из базы данных
    return render(request, 'product_list.html', {'products': products})

# Профиль пользователя
def profile_view(request):
    return render(request, 'profile.html')

# Регистрация клиента
def register_client(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'client'  # Устанавливаем тип пользователя как 'client'
            user.save()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register_client.html', {'form': form})

# Регистрация мастера
def register_master(request):
    if request.method == 'POST':
        form = MasterRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            master = form.save(commit=False)
            user = request.user  # Получаем текущего пользователя
            master.user = user  # Привязываем мастера к пользователю
            master.save()
            return redirect('profile')  # Перенаправление на профиль
    else:
        form = MasterRegistrationForm()
    
    return render(request, 'register_master.html', {'form': form})

# Профиль клиента
def client_profile(request):
    orders = Order.objects.filter(client=request.user)  # Получаем все заказы текущего клиента
    return render(request, 'client_profile.html', {'orders': orders})  # Отображаем профиль с заказами

# Профиль мастера
def master_profile(request):
    master = Master.objects.get(user=request.user)  # Получаем профиль мастера по текущему пользователю
    reviews = Review.objects.filter(master=master)  # Получаем все отзывы для этого мастера
    return render(request, 'master_profile.html', {'master': master, 'reviews': reviews})

# Просмотр мастера для бронирования
def view_master(request, master_id):
    # Получаем объект мастера по его ID
    master = get_object_or_404(Master, id=master_id)
    
    if request.method == 'POST':
        # Если это POST-запрос, создаем заказ
        order_time = request.POST.get('order_time')  # Получаем время заказа из формы
        if order_time:
            Order.objects.create(client=request.user, master=master, time=order_time)
            return redirect('client_profile')  # Перенаправление в профиль клиента

    return render(request, 'view_master.html', {'master': master})

# Бронирование
def create_order(request, master_id):
    # Получаем объект мастера по его ID
    master = get_object_or_404(Master, id=master_id)
    
    if request.method == 'POST':
        # Если это POST-запрос, создаем заказ
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            # Сохраняем заказ с текущим пользователем и мастером
            order = order_form.save(commit=False)
            order.client = request.user
            order.master = master
            order.save()
            return redirect('client_profile')  # Перенаправление в профиль клиента
    else:
        order_form = OrderForm()

    return render(request, 'create_order.html', {'form': order_form, 'master': master})

# Оставить отзыв
def leave_review(request, master_id):
    # Получаем объект мастера по его ID
    master = get_object_or_404(Master, id=master_id)
    
    if request.method == 'POST':
        # Если это POST-запрос, создаем отзыв
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Сохраняем отзыв с текущим пользователем и мастером
            review = form.save(commit=False)
            review.client = request.user
            review.master = master
            review.save()
            return redirect('master_profile', master_id=master.id)  # Перенаправление на профиль мастера
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'form': form, 'master': master})

# Профиль
@login_required
def profile(request):
    return render(request, 'profile.html')
