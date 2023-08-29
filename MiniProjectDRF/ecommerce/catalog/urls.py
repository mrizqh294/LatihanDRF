from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catalog import views


urlpatterns = format_suffix_patterns([
    path('produk/', views.ProdukViews.as_view({'get': 'list'})),
    path('kategori/', views.KategoriViews.as_view()),
    path('daftar-user/', views.userListViews.as_view()),
]) 

