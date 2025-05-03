from django.contrib import admin

from cart_order.models import *
from ovr_products.models import *

from django import forms
from django.contrib import admin

from users.models import CustomUser
from .models import Product, Category, SubCategory, BookGenre, DeviceBrand

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        genres = cleaned_data.get('genres')
        if category and category.category_type == 'book' and not genres:
            raise forms.ValidationError("Книга должна иметь хотя бы один жанр.")
        return cleaned_data

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    filter_horizontal = ('genres',)
    list_display = ('name', 'category', 'subcategory', 'price', 'quantity')
    list_filter = ('category', 'subcategory')
    search_fields = ('name', 'description')


admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(DeviceBrand)
admin.site.register(BookGenre)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)