from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAdminLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'autofocus': True})
    )