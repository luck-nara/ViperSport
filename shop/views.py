from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .decorators import admin_required, verify_admin
from .forms import (
    AdminLoginForm,
    CategoryForm,
    MemberLoginForm,
    MemberRegisterForm,
    PhoneReportForm,
    ProductForm,
    ProductSearchForm,
)
from .models import Category, Favorite, MemberProfile, Order, OrderItem, PhonePointLog, Product


def get_or_create_profile(user):
    profile, _ = MemberProfile.objects.get_or_create(user=user)
    return profile


# ─── หน้าหลัก & สินค้า ───────────────────────────────────────────

def home(request):
    products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()[:6]
    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
    })


def product_list(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.filter(is_active=True)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        if q:
            products = products.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )
        if category:
            products = products.filter(category=category)
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)

    favorite_ids = set()
    if request.user.is_authenticated:
        profile = get_or_create_profile(request.user)
        favorite_ids = set(
            Favorite.objects.filter(member=profile).values_list('product_id', flat=True)
        )

    return render(request, 'shop/product_list.html', {
        'products': products,
        'form': form,
        'favorite_ids': favorite_ids,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    is_favorite = False
    if request.user.is_authenticated:
        profile = get_or_create_profile(request.user)
        is_favorite = Favorite.objects.filter(member=profile, product=product).exists()
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'is_favorite': is_favorite,
    })


# ─── สมาชิก ─────────────────────────────────────────────────────

def member_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            MemberProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'สมัครสมาชิกสำเร็จ ยินดีต้อนรับสู่ ViperSport!')
            return redirect('home')
    else:
        form = MemberRegisterForm()
    return render(request, 'shop/member_register.html', {'form': form})


def member_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = MemberLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'เข้าสู่ระบบสำเร็จ')
            return redirect(request.GET.get('next', 'home'))
    else:
        form = MemberLoginForm()
    return render(request, 'shop/member_login.html', {'form': form})


def member_logout(request):
    logout(request)
    messages.info(request, 'ออกจากระบบแล้ว')
    return redirect('home')


@login_required
def member_profile(request):
    profile = get_or_create_profile(request.user)
    favorites = Favorite.objects.filter(member=profile).select_related('product')
    orders = Order.objects.filter(member=profile)[:10]
    return render(request, 'shop/member_profile.html', {
        'profile': profile,
        'favorites': favorites,
        'orders': orders,
    })


@login_required
def report_phone(request):
    profile = get_or_create_profile(request.user)
    if profile.phone_verified:
        messages.info(request, 'คุณได้รับแต้มจากการแจ้งเบอร์โทรแล้ว')
        return redirect('member_profile')

    if request.method == 'POST':
        form = PhoneReportForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone'].strip()
            if PhonePointLog.objects.filter(phone=phone).exists():
                messages.error(request, 'เบอร์นี้ถูกใช้รับแต้มแล้ว')
            else:
                profile.phone = phone
                profile.points += settings.POINTS_PER_PHONE
                profile.phone_verified = True
                profile.save()
                PhonePointLog.objects.create(
                    member=profile,
                    phone=phone,
                    points_awarded=settings.POINTS_PER_PHONE,
                )
                messages.success(
                    request,
                    f'แจ้งเบอร์สำเร็จ ได้รับ {settings.POINTS_PER_PHONE} แต้ม!',
                )
                return redirect('member_profile')
    else:
        form = PhoneReportForm()
    return render(request, 'shop/report_phone.html', {'form': form})


@login_required
@require_POST
def toggle_favorite(request, pk):
    product = get_object_or_404(Product, pk=pk)
    profile = get_or_create_profile(request.user)
    fav, created = Favorite.objects.get_or_create(member=profile, product=product)
    if not created:
        fav.delete()
        messages.info(request, f'ยกเลิกตราถูกใจ {product.name}')
    else:
        messages.success(request, f'เพิ่มตราถูกใจ {product.name}')
    next_url = request.POST.get('next', 'product_list')
    return redirect(next_url)


# ─── ตะกร้า & สั่งซื้อ (เงินสดเท่านั้น) ─────────────────────────

def _get_cart(request):
    return request.session.setdefault('cart', {})


@login_required
@require_POST
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    if product.stock < 1:
        messages.error(request, 'สินค้าหมด')
        return redirect('product_detail', pk=pk)
    cart = _get_cart(request)
    key = str(pk)
    qty = cart.get(key, {}).get('qty', 0) + 1
    if qty > product.stock:
        messages.error(request, 'จำนวนเกินสต็อก')
        return redirect('product_detail', pk=pk)
    cart[key] = {'qty': qty, 'name': product.name, 'price': str(product.price)}
    request.session.modified = True
    messages.success(request, f'เพิ่ม {product.name} ลงตะกร้า')
    return redirect(request.POST.get('next', 'cart'))


@login_required
def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0')
    for pid, data in cart.items():
        product = Product.objects.filter(pk=int(pid), is_active=True).first()
        if not product:
            continue
        qty = min(data['qty'], product.stock)
        subtotal = product.price * qty
        total += subtotal
        items.append({'product': product, 'qty': qty, 'subtotal': subtotal})
    return render(request, 'shop/cart.html', {'items': items, 'total': total})


@login_required
@require_POST
def cart_remove(request, pk):
    cart = _get_cart(request)
    cart.pop(str(pk), None)
    request.session.modified = True
    messages.info(request, 'ลบสินค้าออกจากตะกร้า')
    return redirect('cart')


@login_required
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, 'ตะกร้าว่าง')
        return redirect('product_list')

    profile = get_or_create_profile(request.user)
    items = []
    total = Decimal('0')
    for pid, data in list(cart.items()):
        product = get_object_or_404(Product, pk=int(pid), is_active=True)
        qty = min(data['qty'], product.stock)
        if qty < 1:
            continue
        subtotal = product.price * qty
        total += subtotal
        items.append({'product': product, 'qty': qty, 'subtotal': subtotal})

    if request.method == 'POST':
        if not items:
            messages.error(request, 'ไม่มีสินค้าในตะกร้า')
            return redirect('cart')
        order = Order.objects.create(
            member=profile,
            total=total,
            status='pending',
            payment_method='cash',
            note=request.POST.get('note', ''),
        )
        for item in items:
            p = item['product']
            OrderItem.objects.create(
                order=order,
                product=p,
                quantity=item['qty'],
                unit_price=p.price,
            )
            p.stock -= item['qty']
            p.save()
        request.session['cart'] = {}
        messages.success(
            request,
            f'สั่งซื้อสำเร็จ #{order.pk} — ชำระเงินสดที่หน้าร้าน',
        )
        return redirect('order_detail', pk=order.pk)

    return render(request, 'shop/checkout.html', {
        'items': items,
        'total': total,
        'payment_method': 'เงินสดเท่านั้น',
    })


@login_required
def order_detail(request, pk):
    profile = get_or_create_profile(request.user)
    order = get_object_or_404(Order, pk=pk, member=profile)
    return render(request, 'shop/order_detail.html', {'order': order})


# ─── แอดมิน (hard-coded login) ───────────────────────────────────

def admin_login_view(request):
    if request.session.get('is_viper_admin'):
        return redirect('admin_dashboard')
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid() and verify_admin(
            form.cleaned_data['username'],
            form.cleaned_data['password'],
        ):
            request.session['is_viper_admin'] = True
            messages.success(request, 'เข้าสู่ระบบแอดมิน')
            return redirect('admin_dashboard')
        messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = AdminLoginForm()
    return render(request, 'shop/admin/login.html', {'form': form})


def admin_logout_view(request):
    request.session.pop('is_viper_admin', None)
    messages.info(request, 'ออกจากระบบแอดมิน')
    return redirect('home')


@admin_required
def admin_dashboard(request):
    return render(request, 'shop/admin/dashboard.html', {
        'product_count': Product.objects.count(),
        'order_count': Order.objects.count(),
        'member_count': MemberProfile.objects.count(),
    })


@admin_required
def admin_product_list(request):
    form = ProductSearchForm(request.GET or None)
    products = Product.objects.all()
    if form.is_valid():
        q = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        if q:
            products = products.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )
        if category:
            products = products.filter(category=category)
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)
    return render(request, 'shop/admin/product_list.html', {
        'products': products,
        'form': form,
    })


@admin_required
def admin_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มสินค้าสำเร็จ')
            return redirect('admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'shop/admin/product_form.html', {
        'form': form,
        'title': 'เพิ่มสินค้า',
    })


@admin_required
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขสินค้าสำเร็จ')
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/admin/product_form.html', {
        'form': form,
        'title': 'แก้ไขสินค้า',
        'product': product,
    })


@admin_required
def admin_product_delete_confirm(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/admin/product_delete_confirm.html', {
        'product': product,
    })


@admin_required
@require_POST
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.success(request, f'ลบสินค้า "{name}" แล้ว')
    return redirect('admin_product_list')


@admin_required
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/admin/category_list.html', {'categories': categories})


@admin_required
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มหมวดหมู่สำเร็จ')
            return redirect('admin_category_list')
    else:
        form = CategoryForm()
    return render(request, 'shop/admin/category_form.html', {
        'form': form,
        'title': 'เพิ่มหมวดหมู่',
    })


@admin_required
def admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขหมวดหมู่สำเร็จ')
            return redirect('admin_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'shop/admin/category_form.html', {
        'form': form,
        'title': 'แก้ไขหมวดหมู่',
        'category': category,
    })


@admin_required
def admin_category_delete_confirm(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'shop/admin/category_delete_confirm.html', {
        'category': category,
    })


@admin_required
@require_POST
def admin_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    name = category.name
    category.delete()
    messages.success(request, f'ลบหมวดหมู่ "{name}" แล้ว')
    return redirect('admin_category_list')


@admin_required
def admin_order_list(request):
    orders = Order.objects.select_related('member__user').all()
    return render(request, 'shop/admin/order_list.html', {'orders': orders})


@admin_required
@require_POST
def admin_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    status = request.POST.get('status')
    if status in dict(Order.STATUS_CHOICES):
        order.status = status
        order.save()
        messages.success(request, f'อัปเดตสถานะคำสั่งซื้อ #{order.pk}')
    return redirect('admin_order_list')


@admin_required
def admin_member_list(request):
    members = MemberProfile.objects.select_related('user').all()
    return render(request, 'shop/admin/member_list.html', {'members': members})
