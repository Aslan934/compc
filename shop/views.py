from unicodedata import category
from django.shortcuts import redirect, render, get_object_or_404, reverse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, ProductSpecificationValue
from order.models import Order, OrderItem


class ItemsListView(ListView):
    model = Product
    template_name = 'index.html'

   # paginate_by = 5


class ItemDetailView(DetailView):
    model = Product
    template_name = 'detail.html'


def search(request):
    keyword = request.GET['search']
    items = Product.objects.filter(title__icontains=keyword)
    types = Category.objects.order_by('name')
    if items:
        messages.info(request, f"{keyword} üçün axtarış nəticələri:")
    else:
        messages.info(request, f"{keyword} üçün heç bir məhsul tapılmadı")
    return render(request, 'search.html', {'object_list': items, 'types': types})


def categories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = Product.objects.filter(category__name=category)

    return render(request, 'categories.html', {'category': category, 'object_list': items})


@ login_required
def favourite_add(request, slug):
    if 'fav' in request.GET:
        item = get_object_or_404(Product, slug=slug)
        if item.favourites.filter(id=request.user.id).exists():
            item.favourites.remove(request.user.id)
        else:
            item.favourites.add(request.user)

    return HttpResponseRedirect(reverse('shop:product_detail', args=(slug,)))


@ login_required
def favorite_list(request):

    user = request.user
    favorite_posts = Product.objects.filter(favourites=request.user)
    context = {
        'favorite_posts': favorite_posts
    }
    print(favorite_posts)
    return render(request, 'favorites.html', context)
