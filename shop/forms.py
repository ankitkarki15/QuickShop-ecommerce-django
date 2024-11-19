from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Import your custom User model

class RegistrationForm(UserCreationForm):
    # Include the fields you want
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User  # Use your custom User model
        fields = ['first_name', 'last_name', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone_number
