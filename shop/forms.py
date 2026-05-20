from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Product


class MemberRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='อีเมล')
    first_name = forms.CharField(max_length=100, label='ชื่อ', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'password1', 'password2')


class MemberLoginForm(AuthenticationForm):
    username = forms.CharField(label='ชื่อผู้ใช้')
    password = forms.CharField(widget=forms.PasswordInput, label='รหัสผ่าน')


class PhoneReportForm(forms.Form):
    phone = forms.CharField(
        max_length=20,
        label='เบอร์โทรศัพท์',
        widget=forms.TextInput(attrs={'placeholder': '08xxxxxxxx'}),
    )


class ProductSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label='คำค้นหา',
        widget=forms.TextInput(attrs={'placeholder': 'ชื่อสินค้า...'}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='ทุกหมวดหมู่',
        label='หมวดหมู่',
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        label='ราคาต่ำสุด',
        widget=forms.NumberInput(attrs={'placeholder': '0'}),
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        label='ราคาสูงสุด',
        widget=forms.NumberInput(attrs={'placeholder': '99999'}),
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class AdminLoginForm(forms.Form):
    username = forms.CharField(label='ชื่อผู้ใช้แอดมิน')
    password = forms.CharField(widget=forms.PasswordInput, label='รหัสผ่าน')
