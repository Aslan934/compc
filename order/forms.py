from django import forms


class OrderForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20, label='', widget=forms.Textarea(attrs={'rows': 2}))
