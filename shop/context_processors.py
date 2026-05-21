def cart_context(request):
    cart = request.session.get('cart', {})
    count = sum(item.get('qty', 0) for item in cart.values())
    return {'cart_count': count}


def nav_active(request):
    """คืนค่าสำหรับไฮไลต์เมนูหน้าปัจจุบัน"""
    match = getattr(request, 'resolver_match', None)
    name = match.url_name if match else ''
    path = request.path

    return {
        'nav_home_active': name == 'home' or path == '/',
        'nav_products_active': name in ('product_list', 'product_detail'),
        'nav_profile_active': name in ('member_profile', 'report_phone', 'order_detail'),
        'nav_cart_active': name in ('cart', 'checkout'),
        'nav_login_active': name == 'member_login',
        'nav_register_active': name == 'member_register',
        'nav_admin_active': path.startswith('/manage/'),
        'nav_admin_dashboard_active': name == 'admin_dashboard',
        'nav_admin_products_active': name in (
            'admin_product_list',
            'admin_product_create',
            'admin_product_edit',
            'admin_product_delete_confirm',
            'admin_product_delete',
        ),
        'nav_admin_categories_active': name in (
            'admin_category_list',
            'admin_category_create',
            'admin_category_edit',
            'admin_category_delete_confirm',
            'admin_category_delete',
        ),
        'nav_admin_orders_active': name in ('admin_order_list', 'admin_order_status'),
        'nav_admin_members_active': name == 'admin_member_list',
    }
