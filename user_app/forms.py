from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ItemFromURL(forms.Form):
    item_url = forms.CharField(label='URL gry', max_length=250)


class Search(forms.Form):
    szukaj = forms.CharField(label=False, max_length=250, required=False)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class AppointCall(forms.Form):
    caller2 = forms.CharField(max_length=8, label="Callee number")
