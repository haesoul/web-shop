from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *
from ovr_products.models import *
from .models import Cart


class CartItemView(ListView):
    model = CartItem
    template_name = 'cart/cart_view.html'
    context_object_name = 'cart'
    form_class = CartItemForm
    success_url = reverse_lazy('cart_items_view')




    def dispatch(self, request, *args, **kwargs):
        # Проверка, что пользователь авторизован
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправить на страницу входа, если пользователь не авторизован
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Получаем все товары в корзине текущего пользователя
        return CartItem.objects.filter(cart__user=self.request.user)

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('delete_item_id')

        if item_id:
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            item.delete()

        # Если запрос на оформление заказа
        if request.POST.get('place_order'):
            return self.place_order(request)

        return redirect('home')

    def place_order(self, request):
        # Получаем корзину текущего пользователя
        cart_items = CartItem.objects.filter(cart__user=request.user)

        # Создаем заказ
        order = Order.objects.create(user=request.user, status='pending')

        # Добавляем товары из корзины в заказ
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price  # Цена товара из модели Product
            )

        # После оформления заказа, очищаем корзину
        cart_items.delete()

        # Перенаправляем пользователя на страницу с подтверждением заказа или страницу заказа
        return redirect('order:order_detail', pk=order.id)



class AddOrderView(LoginRequiredMixin,CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/add_order.html'


    def get_object(self):
        slug = self.kwargs.get('slug')
        return Product.objects.get(slug=slug)

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        cart = Cart.objects.get(user=self.request.user)
        product = self.get_object()

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            messages.error(self.request, "Выбранный товар отсутствует в корзине.")
            return redirect('home')  # или на 'cart:view', если у тебя есть такой маршрут

        # Создаём OrderItem
        OrderItem.objects.create(
            order=self.object,
            product=product,
            quantity=cart_item.quantity,
            price=product.price
        )

        cart_item.delete()  # удаляем товар из корзины после заказа

        return response



    def get_success_url(self):
        return reverse_lazy('home')



class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()  # <-- вот эта строка
        return context


