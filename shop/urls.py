
from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.ItemsListView.as_view(), name='index'),
    path('detail/<str:slug>/', views.ItemDetailView.as_view(), name='product_detail'),
    path('fav/<str:slug>/', views.favourite_add, name='favourites'),
    path('search/', views.search, name='search'),
    path('favourites/', views.favorite_list, name='favorite_list'),
    path('<str:slug>/', views.categories, name='categories'),
]
