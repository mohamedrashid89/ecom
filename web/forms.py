from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
from django.forms import widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        
        exclude = ("timestamp",)
        widgets = {
            "name": widgets.TextInput(attrs={"class": "required form-control", "placeholder": "Your Name"}),
            "phone": widgets.TextInput(attrs={"class": "required form-control", "placeholder": "Your Phone"}),
            "email": widgets.EmailInput(attrs={"class": "required form-control","placeholder": "Your Email Address",}),
            "message": widgets.Textarea(attrs={"class": "required form-control","placeholder": "Type Your Message",}),
        }



class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))
    
    class Meta:
        model = ProductReview
        fields = ['review', 'rating']