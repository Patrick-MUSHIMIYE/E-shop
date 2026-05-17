from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Street address', 'rows': 2}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    zip_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'ZIP / Postal code'}))
    card_number = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    card_expiry = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    card_cvv = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))
