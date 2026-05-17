from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import RegisterForm, CheckoutForm


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def product_list(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_cart(request)
    size = request.POST.get('size', 'M')
    quantity = int(request.POST.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(cart=cart, product=product, size=size)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    messages.success(request, f'{product.name} ({size}) added to cart.')
    return redirect(request.POST.get('next', 'store:cart'))


def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    cart = get_or_create_cart(request)
    if item.cart == cart:
        item.delete()
    return redirect('store:cart')


def cart_update(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    cart = get_or_create_cart(request)
    if item.cart == cart:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect('store:cart')


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')

    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=form.cleaned_data['full_name'],
            email=form.cleaned_data['email'],
            address=form.cleaned_data['address'],
            city=form.cleaned_data['city'],
            zip_code=form.cleaned_data['zip_code'],
            total=cart.get_total(),
        )
        for ci in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                product_name=ci.product.name,
                size=ci.size,
                quantity=ci.quantity,
                price=ci.product.get_display_price(),
            )
        cart.items.all().delete()
        messages.success(request, f'Order #{order.pk} placed successfully!')
        return redirect('store:order_confirm', pk=order.pk)

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


def order_confirm(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'store/order_confirm.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})


def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.username}!')
        return redirect('store:home')
    return render(request, 'registration/register.html', {'form': form})
