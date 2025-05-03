from django import forms
from django.template.context_processors import request

from .models import *


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product','quantity']

        widgets = {
            'product': forms.HiddenInput(attrs={'class': 'form-control'}),

            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', }),
        }

        def clean_quantity(self):
            quantity = self.cleaned_data.get('quantity')
            if quantity <= 0:
                raise forms.ValidationError("Количество товаров должно быть выше 0")

            return quantity


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address','billing_address', 'status']  # Не включаем 'user', так как он будет автоматически передаваться



class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # При изменении товара, автоматически подставляем цену из модели Product
            if self.instance and self.instance.product:
                self.fields['price'].initial = self.instance.product.price

        def save(self, commit=True):
            instance = super().save(commit=False)
            if instance.product:
                instance.price = instance.product.price  # Подставляем цену из модели Product
            if commit:
                instance.save()
            return instance


