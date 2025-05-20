# views.py
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Profile, Cart, CartItem
from django.template.loader import render_to_string

def index(request):
    if request.user.is_authenticated:
        print('aaaaa')
    query = request.GET.get('q', '').strip()

    if query:
        grouped = Product.objects.fuzzy_search_grouped_by_shop(query)

        context = {
            'vkusvile_data': grouped.get('Vkuss_vill', []),
            'av_data': grouped.get('Asbuka Vkusa', []),
            'perekrestok_data': grouped.get('perekrestok', []),
            'query': query,

            'stores': [
                {
                    'name': 'Вкусвилл',
                    'logo': 'https://avatars.mds.yandex.net/i?id=6096edcf21e822536400b8bbf3b7279580e0d45e-11386386-images-thumbs&n=13',
                    'products': grouped.get('Vkuss_vill', [])
                },
                {
                    'name': 'Перекресток',
                    'logo': 'https://avatars.mds.yandex.net/i?id=2642bb99605d0428fbf7533881b03e946e1b8b80-5189723-images-thumbs&n=13',
                    'products': grouped.get('perekrestok', [])
                },
                {
                    'name': 'Азбука вкуса',
                    'logo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-TiXjDBJvN80GfDR9QhHo4TRqadtw-mV3zQ&s',
                    'products' : grouped.get('Asbuka Vkusa', [])
                },
            ],
            'cart': get_cart_context(request.user) if request.user.is_authenticated else [],
            'modal_product': {
                'name': 'Авокадо хасс Самокат, импорт в две строки',
                'img_url': 'https://main-cdn.sbermegamarket.ru/big1/hlr-system/292/311/849/101/220/22/100042521002b0.jpg',
                'new_price': 8999,
                'price': 10000,
                'count': 1,
                'measure': '1 литр',
                'image': 'https://avatars.mds.yandex.net/i?id=6096edcf21e822536400b8bbf3b7279580e0d45e-11386386-images-thumbs&n=13',
                'store_url': 'https://vkusvill.ru/',
                'id': 1,
            },
        }
    else:
        # Стандартный режим — показываем скидки
        context = {
            'stores': [
                {
                    'name': 'Вкусвилл',
                    'logo': 'https://avatars.mds.yandex.net/i?id=6096edcf21e822536400b8bbf3b7279580e0d45e-11386386-images-thumbs&n=13',
                    'delivery_time': '15-30',
                    'products': Product.objects.get_sales_by_id(1)
                },
                {
                    'name': 'Перекресток',
                    'logo': 'https://avatars.mds.yandex.net/i?id=2642bb99605d0428fbf7533881b03e946e1b8b80-5189723-images-thumbs&n=13',
                    'delivery_time': '15-30',
                    'products': Product.objects.get_sales_by_id(4)
                },
                {
                    'name': 'Азбука вкуса',
                    'logo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-TiXjDBJvN80GfDR9QhHo4TRqadtw-mV3zQ&s',
                    'delivery_time': '15-30',
                    'products': Product.objects.get_sales_by_id(3)
                },
            ],
            'cart': get_cart_context(request.user) if request.user.is_authenticated else [],
            'modal_product': {
                'name': 'Авокадо хасс Самокат, импорт в две строки',
                'store': {
                    'name': 'Вкусвилл',
                    'logo': 'https://avatars.mds.yandex.net/i?id=6096edcf21e822536400b8bbf3b7279580e0d45e-11386386-images-thumbs&n=13',
                },
                'img_url': 'https://main-cdn.sbermegamarket.ru/big1/hlr-system/292/311/849/101/220/22/100042521002b0.jpg',
                'new_price': 8999,
                'price': 10000,
                'count': 1,
                'measure': '1 литр',
                'image': 'https://avatars.mds.yandex.net/i?id=6096edcf21e822536400b8bbf3b7279580e0d45e-11386386-images-thumbs&n=13',
                'store_url': 'https://vkusvill.ru/',
                'id': 1,
            },
        }

    return render(request, 'index.html', context)

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Profile, Cart
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        errors = {}

        # Валидация
        if not firstname:
            errors['firstname'] = "Введите имя"

        if not email:
            errors['email'] = "Введите email"
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = "Некорректный email"
            if User.objects.filter(username=email).exists():
                errors['email'] = "Пользователь с таким email уже зарегистрирован"

        if not phone:
            errors['phone'] = "Введите номер телефона"

        if not password1 or not password2:
            errors['password'] = "Введите оба пароля"
        elif password1 != password2:
            errors['password'] = "Пароли не совпадают"
        elif len(password1) < 8:
            errors['password'] = "Пароль должен быть не менее 8 символов"

        if errors:
            # Возврат формы с ошибками и введёнными данными
            return render(request, 'registration.html', {
                'errors': errors,
                'values': {
                    'firstname': firstname,
                    'email': email,
                    'phone': phone,
                }
            })

        try:
            user = User.objects.create_user(
                username=email,
                first_name=firstname,
                email=email,
                password=password1
            )
            Profile.objects.create(
                user=user,
                phone_number=phone,
                email=email
            )
            user = authenticate(request, username=email, password=password1)
            if user is not None:
                login(request, user)
                Cart.objects.get_or_create(user=user)
            return redirect('/')
        except IntegrityError:
            errors['general'] = "Произошла ошибка при создании пользователя"
            return render(request, 'registration.html', {
                'errors': errors,
                'values': {
                    'firstname': firstname,
                    'email': email,
                    'phone': phone,
                }
            })

    return render(request, 'registration.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {
                'errors': {'general': 'Неверный email или пароль'},
                'values': {'username': email}
            })

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def get_cart_context(user):
    if not user.is_authenticated:
        return []

    cart, _ = Cart.objects.get_or_create(user=user)
    items = CartItem.objects.select_related('product__shop').filter(cart=cart)

    from collections import defaultdict
    grouped = defaultdict(lambda: {'store': {}, 'products': [], 'total_price': 0, 'delivery_time': '15-30'})
    names_links = {'perekrestok':['https://avatars.mds.yandex.net/i?id=2642bb99605d0428fbf7533881b03e946e1b8b80-5189723-images-thumbs&n=13', 'Перекресток'],
                   'Asbuka Vkusa':['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-TiXjDBJvN80GfDR9QhHo4TRqadtw-mV3zQ&s', 'Азбука Вкуса'],
                   'Vkuss_vill':['https://avatars.mds.yandex.net/i?id=6096edcf21e822536400b8bbf3b7279580e0d45e-11386386-images-thumbs&n=13', 'Вкуссвил']}
    for item in items:
        shop = item.product.shop
        grouped[shop.name]['store'] = {
            'name': names_links[shop.name][1],
            'logo': names_links[shop.name][0],
        }
        grouped[shop.name]['products'].append({
            'name': item.product.name,
            'img_url': item.product.image,
            'price': item.product.last_price or item.product.price,
            'count': item.quantity,
            'measure': item.product.weight,
            'id': item.product.id,
        })
        grouped[shop.name]['total_price'] += (item.product.last_price or item.product.price) * item.quantity

    return list(grouped.values())

@login_required
def cart_view_partial(request):
    context = {'cart': get_cart_context(request.user)}
    html = render_to_string('components/cart.html', context, request=request)
    return HttpResponse(html)

@login_required
@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()

    return JsonResponse({'status': 'ok'})

@login_required
@require_POST
def increase_quantity(request):
    product_id = request.POST.get('product_id')
    cart, _ = Cart.objects.get_or_create(user=request.user)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        item.quantity += 1
        item.save()
    except CartItem.DoesNotExist:
        pass
    return JsonResponse({'status': 'ok'})

@login_required
@require_POST
def decrease_quantity(request):
    product_id = request.POST.get('product_id')
    cart, _ = Cart.objects.get_or_create(user=request.user)
    try:
        item = CartItem.objects.get(cart=cart, product_id=product_id)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    except CartItem.DoesNotExist:
        pass
    return JsonResponse({'status': 'ok'})

def sales_cards(request):
    if request.method == 'POST':
        print("Здесь логика доавления краты")
    else:
        return render(request, 'sales_cards.html')

def delete_profile(request):
    if request.method == 'POST':
        print("Здесь логика удаления аккаунта")
    else:
        return render(request, 'delete_profile.html')

def help(request):
    if request.method == 'POST':
        print('Здесь логика обработки формы для поддержки')
    else:
        return render(request, 'help.html')

def favorites(request):
    if request.method == 'POST':
        print('Здесь логика добавления товара в избранное')
    if request.method == 'DELETE':
        print('Здесь логика удаления товара из избранного')
    return render(request, 'favorites.html')

def list_view(request):
    if request.method == 'POST':
        print('Здесь логика создания новой корзины')
    return render(request, 'lists_info.html')


def list_edit(request,id):
    if request.method == 'POST':
        print('Здесь логика добавления нового товара в список')

def product_info(request,id):
    return render(request,'product_info.html')
