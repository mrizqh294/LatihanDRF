from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from catalog import views

products = views.ProdukViews.as_view({
    'get': 'list', 
    'post' : 'create',
    })

# product = views.ProdukViews.as_view({

# })


urlpatterns = format_suffix_patterns([
    path('products/', products, name="products" ),
    path('products/<int:pk>',views.ProdukViews.as_view({'get': 'retrieve', 'put' : 'update'})),
    path('kategori/', views.KategoriViews.as_view()),
    path('users/', views.userListViews.as_view()),
]) 

