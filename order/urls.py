
from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('cart/<str:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<str:slug>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('delete_order/<int:id>/',
         views.delete_order, name='delete_order'),
]
