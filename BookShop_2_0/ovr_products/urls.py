from django.urls import path

from ovr_products.views import *
app_name = 'main'
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product-detail/<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    path('select-category/',CategoriesForSelectView.as_view(),name='select_category'),
    path('category/<slug:category_slug>/',ProductByCategoryView.as_view(),name='products_by_category'),
    path('category/<slug:category_slug>/<slug:sub_category_slug>/',ProductByCategoryView.as_view(),name='products_by_category_subcategory'),
    path('category/<slug:category_slug>/<slug:sub_category_slug>/genre/<slug:genre_slug>/',ProductByCategoryView.as_view(),name='products_by_book_genre'),
    path('book/genre/<slug:genre_slug>/',ProductByBookGenreView.as_view(),name='only_genre_ordering'),
    path('devices/brand/<slug:brand_slug>/', DeviceBrandFilterView.as_view(), name='device_brand_filter'),
    path('devices/brand/<slug:subcategory_slug>/<slug:brand_slug>/', DeviceBrandFilterView.as_view(), name='device_brand_filter_with_subcategory'),
    path('search/', search_results, name='search'),




]

