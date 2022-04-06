from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse
from order.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from shop.models import Product
from django.contrib import messages
from datetime import timezone
from order.forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist


def cart(request):
    context = {}
    if request.user.is_authenticated:
        new_order, created = Order.objects.get_or_create(
            user=request.user, ordered=False)

        confirmed_order = Order.objects.filter(
            user=request.user, ordered=True).order_by('-date_ordered')

    else:
        if not request.session.exists(request.session.session_key):
            request.session.create()

        new_order, created = Order.objects.get_or_create(
            user=None, session_key=request.session.session_key, ordered=False)

        confirmed_order = Order.objects.filter(
            session_key=request.session.session_key, ordered=True).order_by('-date_ordered')

    if request.method == 'POST':
        if new_order.items.exists():
            new_order.phone_number = request.POST['phone_number']
            new_order.name = request.POST['name']
            new_order.surname = request.POST['surname']
            new_order.ordered = True
            new_order.save()
            messages.info(request, 'Sifarişiniz qeydə alındı')
        else:
            messages.info(request, 'Səbətdə məhsul yoxdur')
    context = {'order': new_order, 'confirmed_order': confirmed_order}

    return render(request, 'cart.html', context)


def add_to_cart(request, slug):
    if request.method == 'POST':
        if 'add_to_cart' or 'order_now' in request.POST:
            if request.user.is_authenticated:
                order_qs = Order.objects.get_or_create(
                    user=request.user, ordered=False)
            else:

                if not request.session.exists(request.session.session_key):
                    request.session.create()

                order_qs = Order.objects.get_or_create(
                    user=None, session_key=request.session.session_key, ordered=False)

            order = order_qs[0]
            item = get_object_or_404(Product, slug=slug)

            order_item, created = order.items.all().get_or_create(product=item)

        if order.items.filter(product__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "Məhsul səbətə əlavə olundu.")
        else:
            order.items.add(order_item)
            messages.warning(request, "Məhsul səbətə əlavə olundu.")

    if 'add_to_cart' in request.POST:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif 'order_now' in request.POST:
        return redirect("order:cart")


def remove_from_cart(request, slug):
    if request.method == 'POST' and 'remove' in request.POST:
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(user=request.user, ordered=False)
            else:
                order = Order.objects.get(
                    user=None, session_key=request.session.session_key, ordered=False)

            item = get_object_or_404(Product, slug=slug)
            order_item = order.items.all().get(product=item)

            if order.items.filter(product__slug=item.slug).exists():
                order_item.delete()
                messages.info(request, "Məhsul səbətdən silindi.")
                return redirect("order:cart")

        except ObjectDoesNotExist:
            messages.info(request, "Məhsul səbətdən mövcud deyil")

    else:
        messages.info(request, "Sifarişiniz yoxdur")
    return redirect('order:cart')


def delete_order(request, id):
    if request.method == 'POST' and 'delete_order' in request.POST:

        if request.user.is_authenticated:
            order = Order.objects.get(
                user=request.user, ordered=True, id=id)
        else:
            order = Order.objects.get(
                user=None, session_key=request.session.session_key, ordered=True, id=id)

        order.delete()
        messages.info(request, "Sifarişiniz silindi")

    return redirect('order:cart')
