from email import message
from unicodedata import category
from django.shortcuts import redirect, render, get_object_or_404, reverse, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category, ProductSpecificationValue, Banner, Contact
from order.models import Order, OrderItem


class ItemsListView(ListView):
    template_name = 'index.html'

    def get_queryset(self):
        banners = Banner.objects.all()
        return banners
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = self.get_queryset()
        return context


class ItemDetailView(DetailView):
    model = Product
    template_name = 'detail.html'


def search(request):
    keyword = request.GET['search']
    items = Product.objects.filter(title__icontains=keyword)

    if items:
        messages.info(request, f"{keyword} üçün axtarış nəticələri:")
    else:
        messages.info(request, f"{keyword} üçün heç bir məhsul tapılmadı")

    return render(request, 'search.html', {'object_list': items})


def categories(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = Product.objects.filter(category__name=category)
    p = Paginator(items, 20)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    return render(request, 'categories.html', {'category': category, 'object_list': items, 'page_obj': page_obj})


@ login_required
def favourite_add(request, slug):
    if request.method == 'POST' and 'add_to_favorites' in request.POST:
        item = get_object_or_404(Product, slug=slug)
        if item.favourites.filter(id=request.user.id).exists():
            item.favourites.remove(request.user.id)
            messages.info(request, "Seçilmişlər listindən çıxardıldı")
        else:
            item.favourites.add(request.user)
            messages.warning(request, "Seçilmişlər listinə əlavə olundu")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@ login_required
def favorite_list(request):

    user = request.user
    favorite_posts = Product.objects.filter(favourites=request.user)
    context = {
        'favorite_posts': favorite_posts
    }
    return render(request, 'favorites.html', context)


def contact(request):
    new_feedback = Contact()
    if request.method == 'POST':
        new_feedback.name = request.POST['name']
        new_feedback.email = request.POST['email']
        new_feedback.phone_number = request.POST['phone_number']
        new_feedback.message = request.POST['message']
        new_feedback.save()
        messages.warning(request, "Müraciətiniz qeydə alındı")
    return render(request, 'contact.html')
