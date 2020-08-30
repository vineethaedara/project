from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    class Meta:
        model=Account
        fields=['username','email','phonenumber','gender','adhaarnumber','location','DateOfBirth' ]

class LoginForm(forms.ModelForm):
    email=forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=Account
        fields=['email','password']

    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError('Invalid User Credentials')
        