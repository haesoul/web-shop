from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from cart_order.forms import CartItemForm
from cart_order.models import *
from ovr_products.forms import SearchForm
from ovr_products.models import *


class HomeView(ListView):
    model = Product
    template_name = 'ovr_products/home.html'
    context_object_name = 'products'
    paginate_by = 10



class ProductDetailView(FormMixin,DetailView):
    template_name = 'ovr_products/product_detail.html'
    model = Product
    context_object_name = 'product'
    form_class = CartItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["initial"] = {"product": self.get_object()}
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            product = form.cleaned_data["product"]
            quantity = form.cleaned_data["quantity"]

            # Получаем корзину пользователя или создаём новую
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Добавляем товар в корзину (обновляем количество, если уже есть)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            cart_item.save()

            return redirect("home")  # Перенаправляем в корзину

        return self.get(request, *args, **kwargs)


class CategoriesForSelectView(ListView):
    model = Category
    template_name = 'ovr_products/category_for_select.html'
    context_object_name = 'categories'

class ProductByCategoryView(ListView):
    model = Product
    template_name = 'ovr_products/category_ordering.html'
    context_object_name = 'products'
    paginate_by = 10
    def dispatch(self, request, *args, **kwargs):
        self.category = self.get_category()
        self.subcategory = self.get_subcategory()
        self.genre = self.get_genre()
        return super().dispatch(request, *args, **kwargs)

    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs['category_slug'])

    def get_subcategory(self):
        slug = self.kwargs.get('sub_category_slug')
        if slug:
            return get_object_or_404(SubCategory, slug=slug, category=self.category)
        return None

    def get_genre(self):
        slug = self.kwargs.get('genre_slug')
        if slug and self.category.category_type == 'book':
            return get_object_or_404(BookGenre, slug=slug)
        return None

    def get_queryset(self):
        queryset = Product.objects.filter(category=self.category)

        if self.subcategory:
            queryset = queryset.filter(subcategory=self.subcategory)

        if self.genre:
            queryset = queryset.filter(genres=self.genre)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.distinct()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category': self.category,
            'categories': Category.objects.all(),
            'category_selected': self.category.slug,
            'sub_category_selected': self.subcategory.slug if self.subcategory else None,
            'genre_selected': self.genre.slug if self.genre else None,
            'genres': BookGenre.objects.all(),
            'subcategories': SubCategory.objects.all(),
            'subcategory': self.subcategory,
            'genre': self.genre,
            'brands': DeviceBrand.objects.all()
        })

        return context




class ProductByBookGenreView(ListView):
    model = Product
    template_name = 'ovr_products/only_book_genre_ordering.html'
    context_object_name = 'products'
    paginate_by = 10
    def dispatch(self, request, *args, **kwargs):
        self.genre = get_object_or_404(BookGenre, slug=self.kwargs['genre_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Product.objects.filter(genres=self.genre).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'categories': Category.objects.all(),
            'genres': BookGenre.objects.all(),
            'genre_selected': self.genre.slug,
            'genre': self.genre,
            'category': Category.objects.filter(category_type="book").first(),
            'brands': DeviceBrand.objects.all()
        })

        return context



class DeviceBrandFilterView(ListView):
    model = Product
    template_name = 'ovr_products/device_brand_filter.html'
    context_object_name = 'products'
    paginate_by = 10
    def get_category(self):
        return get_object_or_404(Category, slug=self.kwargs['category_slug'])
    def get_subcategory(self):
        return get_object_or_404(SubCategory,slug=self.kwargs['sub_category_selected'])

    def get_queryset(self):
        return Product.objects.filter(
            device_brand__slug=self.kwargs['brand_slug'],
            category__category_type='device'  # только устройства
        ).select_related('device_brand', 'category', 'subcategory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_slug'] = self.kwargs['brand_slug']
        context['brands'] = DeviceBrand.objects.all()
        context['categories'] = Category.objects.all()
        subcategory_slug = self.kwargs.get('subcategory')
        context['sub_category_selected'] = get_object_or_404(SubCategory,slug=subcategory_slug )if subcategory_slug else None
        context['category_selected'] = get_object_or_404(Category, slug="device")
        context['category'] = get_object_or_404(Category,slug="device")

        return context

def search_results(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()  # Если нет запроса, то не показываем ничего

    return render(request, 'ovr_products/search_results.html', {
        'query': query,
        'products': products
    })