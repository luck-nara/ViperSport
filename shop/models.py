from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField('หมวดหมู่', max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'หมวดหมู่'
        verbose_name_plural = 'หมวดหมู่'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='หมวดหมู่',
    )
    name = models.CharField('ชื่อสินค้า', max_length=200)
    description = models.TextField('รายละเอียด', blank=True)
    price = models.DecimalField(
        'ราคา (บาท)',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    stock = models.PositiveIntegerField('คงเหลือ', default=0)
    image = models.ImageField('รูปภาพ', upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField('เปิดขาย', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'สินค้า'
        verbose_name_plural = 'สินค้า'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('เบอร์โทร', max_length=20, blank=True)
    points = models.PositiveIntegerField('แต้มสะสม', default=0)
    phone_verified = models.BooleanField('ยืนยันเบอร์แล้ว', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'สมาชิก'
        verbose_name_plural = 'สมาชิก'

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    """ตราถูกใจ — สินค้าที่สมาชิกกดชอบ"""
    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ตราถูกใจ'
        verbose_name_plural = 'ตราถูกใจ'
        unique_together = [['member', 'product']]

    def __str__(self):
        return f'{self.member} ♥ {self.product}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอชำระ'),
        ('paid', 'ชำระเงินสดแล้ว'),
        ('cancelled', 'ยกเลิก'),
    ]
    member = models.ForeignKey(
        MemberProfile,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='สมาชิก',
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(
        'วิธีชำระ',
        max_length=20,
        default='cash',
        editable=False,
    )
    note = models.TextField('หมายเหตุ', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'คำสั่งซื้อ'
        verbose_name_plural = 'คำสั่งซื้อ'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'รายการสั่งซื้อ'

    @property
    def subtotal(self):
        return self.unit_price * self.quantity


class PhonePointLog(models.Model):
    """บันทึกการแจ้งเบอร์โทรเพื่อรับแต้ม"""
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    points_awarded = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'ประวัติแจ้งเบอร์'
