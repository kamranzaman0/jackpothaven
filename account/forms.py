from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)


# forms.py

from django import forms

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=15)


