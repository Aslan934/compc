from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model

User = get_user_model()


def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        'form': form
    }

    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            messages.error(request, 'Email və ya şifrə yanlışdır!')
            return render(request, 'login.html', context)

        login(request, user)
        return redirect('shop:index')
    return render(request, 'login.html', context)


def registerUser(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get("password")
        name = form.cleaned_data.get("name")
        surname = form.cleaned_data.get("surname")

        newUser = User()
        newUser.email = email
        newUser.name = name
        newUser.surname = surname

        newUser.set_password(password)

        newUser.save()
        login(request, newUser)

        return redirect('shop:index')

    context = {
        "form": form
    }
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('shop:index')
