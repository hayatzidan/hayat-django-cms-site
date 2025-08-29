# phone_login_plugin/forms.py
from django import forms
from phonenumber_field.formfields import PhoneNumberField

class PhoneLoginForm(forms.Form):
    phone_number = PhoneNumberField(label='Phone number', widget=forms.TextInput(attrs={'id': 'phone-input'}))
    password = forms.CharField(widget=forms.PasswordInput)