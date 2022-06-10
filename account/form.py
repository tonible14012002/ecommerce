from dataclasses import field
from pyexpat import model
from django import forms
from django.contrib.auth import get_user_model
from account.models import CustomerInfo

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    password = forms.CharField(widget=forms.widgets.PasswordInput,
                               min_length=8,
                               label='Password')
    password_confirm = forms.CharField(widget=forms.widgets.PasswordInput,
                                       min_length=8,
                                       label='Password confirm')
    
    def clean_password_confirm(self):
        password_confirm = self.cleaned_data['password_confirm']
        if password_confirm != self.cleaned_data['password']:
            raise forms.ValidationError('password confirm does not match.')
        return password_confirm

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise forms.ValidationError('This field is required.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise forms.ValidationError('This field is required.')
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email has already be used.')
        return email

class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerInfo
        fields = ['phone', 'address', 'city', 'country']

class LoginForm(forms.Form):
    username = forms.CharField(min_length=5, label='Username or email address')
    password = forms.CharField(min_length=8,label='password', widget=forms.PasswordInput)
    
# class PasswordResetConfirmForm()