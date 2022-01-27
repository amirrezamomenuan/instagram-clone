from . import models
from django import forms

def all_numeric(pas):
    numbers = "0123456789"
    count = 0
    for char in pas:
        if char in numbers:
            count += 1
    if count == len(pas):
        return True
    return False



class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=30)

    password = forms.CharField(max_length=16, min_length=8)
    password_confirmation = forms.CharField(max_length=16, min_length=8)

        
    def clean_username(self):
        if models.User.objects.filter(username = self.cleaned_data['username']).exists():
            raise forms.ValidationError("this is already taken! choose another one please :)")

        return self.cleaned_data['username']
    
    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data['password']
        pass2 = cleaned_data['password_confirmation']

        if pass1 != pass2:
            raise forms.ValidationError("passwords are not maching")
        
        
class phoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=11)

    def clean_phone_number(self):
        number = self.cleaned_data['phone_number']
        if not all_numeric(number):
            raise forms.ValidationError("can onlu use numerical digits")
        
        if models.User.objects.filter(phone_number = number).exists():
            raise forms.ValidationError("this phone number is used before click on signin to continue")

        return number


class codeValidationForm(forms.Form):
    confirmation_code = forms.CharField(max_length=6)