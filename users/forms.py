from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True, label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=255,  label='Email')
    name = forms.CharField(
        max_length=255, label="Ad")
    surname = forms.CharField(
        max_length=255, label="Soyad")
    password = forms.CharField(
        max_length=20, label="Şifrə", widget=forms.PasswordInput)
    confirm = forms.CharField(
        max_length=20, label="Şifrəni təkrarlayın", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        name = self.cleaned_data.get('name')
        surname = self.cleaned_data.get('surname')
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email mövcuddur")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Şifrələr eyni deyil")
        values = {
            "email": email,
            'name': name,
            'surname': surname,
            "password": password,
            "confirm": confirm,
        }
        return values
