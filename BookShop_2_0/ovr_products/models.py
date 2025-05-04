from django.core.exceptions import ValidationError
from django.db import models

from users.models import CustomUser


class Category(models.Model):
    CATEGORY_TYPES = [
        ('book', 'Book'),
        ('device', 'Device'),
        ('accessory', 'Accessory'),
        ('clothing', 'Clothing'),
    ]
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name


class BookGenre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True)

    def __str__(self):
        return self.name


class DeviceBrand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=55, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    slug = models.SlugField(max_length=55, unique=True,db_index=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(max_length=5000)

    category = models.ForeignKey(Category, on_delete=models.CASCADE,db_index=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)

    genres = models.ManyToManyField(BookGenre, blank=True, related_name='products')
    device_brand = models.ForeignKey(DeviceBrand, on_delete=models.CASCADE, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        is_saved = self.pk is not None
        category_type = self.category.category_type

        # Общая проверка соответствия подкатегории и категории
        if self.subcategory and self.subcategory.category != self.category:
            raise ValidationError("Подкатегория должна соответствовать выбранной категории.")

        # Категория: книга
        if category_type == 'book':
            if not self.subcategory:
                raise ValidationError("Книга должна иметь подкатегорию (жанр, тип и т.п.).")
            if self.device_brand:
                raise ValidationError("Книга не должна иметь бренд устройства.")

        # Категория: устройство
        elif category_type == 'device':
            if not self.subcategory:
                raise ValidationError("Устройство должно иметь подкатегорию.")
            if not self.device_brand:
                raise ValidationError("Устройство должно иметь бренд.")
            if is_saved and self.genres.exists():
                raise ValidationError("Устройство не должно иметь жанры.")

        # Категория: аксессуар
        elif category_type == 'accessory':
            if not self.subcategory:
                raise ValidationError("Аксессуар должен иметь подкатегорию.")
            if self.device_brand:
                raise ValidationError("Аксессуар не должен иметь бренд.")
            if is_saved and self.genres.exists():
                raise ValidationError("Аксессуар не должен иметь жанры.")

        # Категория: одежда
        elif category_type == 'clothing':
            if not self.subcategory:
                raise ValidationError("Одежда должна иметь подкатегорию.")
            if self.device_brand:
                raise ValidationError("Одежда не должна иметь бренд.")
            if is_saved and self.genres.exists():
                raise ValidationError("Одежда не должна иметь жанры.")

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('ovr_products.Product', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

