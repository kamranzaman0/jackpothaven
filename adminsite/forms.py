from django import forms
from django.contrib.auth.models import User

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_staff', 'is_superuser']
