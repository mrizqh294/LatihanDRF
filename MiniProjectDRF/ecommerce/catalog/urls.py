from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catalog import views

urlpatterns = [
    path('kategori/', views.KategoriViews.as_view()),
    path('produk/', views.ProdukListViews.as_view()),
    path('daftar-user/', views.userListViews.as_view()),
]