from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    path('register/', views.member_register, name='member_register'),
    path('login/', views.member_login, name='member_login'),
    path('logout/', views.member_logout, name='member_logout'),
    path('profile/', views.member_profile, name='member_profile'),
    path('report-phone/', views.report_phone, name='report_phone'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),

    path('manage/login/', views.admin_login_view, name='admin_login'),
    path('manage/logout/', views.admin_logout_view, name='admin_logout'),
    path('manage/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/products/', views.admin_product_list, name='admin_product_list'),
    path('manage/products/add/', views.admin_product_create, name='admin_product_create'),
    path('manage/products/<int:pk>/edit/', views.admin_product_edit, name='admin_product_edit'),
    path(
        'manage/products/<int:pk>/delete/',
        views.admin_product_delete_confirm,
        name='admin_product_delete_confirm',
    ),
    path('manage/products/<int:pk>/delete/confirm/', views.admin_product_delete, name='admin_product_delete'),
    path('manage/categories/', views.admin_category_list, name='admin_category_list'),
    path('manage/categories/add/', views.admin_category_create, name='admin_category_create'),
    path('manage/categories/<int:pk>/edit/', views.admin_category_edit, name='admin_category_edit'),
    path(
        'manage/categories/<int:pk>/delete/',
        views.admin_category_delete_confirm,
        name='admin_category_delete_confirm',
    ),
    path(
        'manage/categories/<int:pk>/delete/confirm/',
        views.admin_category_delete,
        name='admin_category_delete',
    ),
    path('manage/orders/', views.admin_order_list, name='admin_order_list'),
    path('manage/orders/<int:pk>/status/', views.admin_order_status, name='admin_order_status'),
    path('manage/members/', views.admin_member_list, name='admin_member_list'),
]
