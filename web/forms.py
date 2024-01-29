from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactForm
        
#         exclude = ("timestamp",)
#         widgets = {
#             "name": widgets.TextInput(attrs={"class": "required form-control", "placeholder": "Your Name"}),
#             "phone": widgets.TextInput(attrs={"class": "required form-control", "placeholder": "Your Phone"}),
#             "email": widgets.EmailInput(attrs={"class": "required form-control","placeholder": "Your Email Address",}),
#             "message": widgets.Textarea(attrs={"class": "required form-control","placeholder": "Type Your Message",}),
#         }



class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
        
class CheckoutForm(forms.Form):
    COUNTRY_CHOICES = [
        ('US', 'United States'),
        ('CA', 'Canada'),
        ('GB', 'United Kingdom'),
        ('FR', 'France'),
        ('DE', 'Germany'),
        ('AU', 'Australia'),
        ('IND', 'India'),
        # Add more country choices as needed
    ]

    # Other form fields...

    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    company_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    apartment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apartment'}))
    town_city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Town/City'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State'}))
    zipcode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zipcode'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    
    
    