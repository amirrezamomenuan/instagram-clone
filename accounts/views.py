from django.shortcuts import render, HttpResponse
from . import models, forms
from .utils import phone_number_validator
confirmation_codes = []


def signup_profile_view(request):
    if request.POST.get("confirmation_code"):
        print('stage 3')
        conf_code_form = forms.codeValidationForm(request.POST)
        if conf_code_form.is_valid():
            print('stage 4')
            number = conf_code_form.data['phone_number']

            print(confirmation_codes[-1])
            print(conf_code_form.cleaned_data['confirmation_code'])
            if confirmation_codes[-1][2] and str(confirmation_codes[-1][0]) == conf_code_form.cleaned_data['confirmation_code']:
                print(confirmation_codes[-1])
                print("stage 5")
                form = forms.UserCreationForm()
            
            else:
                form = forms.codeValidationForm()
            content = {"form":form, 'phone_number':number}

            return render(request, 'user_signup_form.html', content)
        
        content = {"form":forms.codeValidationForm, 'phone_number':conf_code_form.data['phone_number'],'form_errors':conf_code_form.errors,}
        return render(request, 'user_signup_form.html', content)
        

    elif request.POST.get('phone_number') and not request.POST.get('username'):
        print("stage 1")
        phone_confirmation_form = forms.phoneNumberForm(request.POST)

        if phone_confirmation_form.is_valid():
            
            print("stage 2")
            number = phone_confirmation_form.cleaned_data['phone_number']
            form = forms.codeValidationForm()
            content = {"form":form, 'phone_number':number}

            sms_result = phone_number_validator(number)
            confirmation_codes.append(sms_result)
            return render(request, 'user_signup_form.html', content)

        form = forms.phoneNumberForm()
        content = {"form":form, 'form_errors':phone_confirmation_form.errors}
        return render(request, 'user_signup_form.html', content)


    elif request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print("-------------------------------forms is valid")
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            phone_number = form.data['phone_number']
            user = models.User(username = username, phone_number = phone_number)
            # user = models.User.objects.create(username = username, phone_number = phone_number)
            user.set_password(password)
            user.save()
            #TODO : this should then change to another path
            return HttpResponse("User created successfully")
        else:
            content = {"form":form, 'phone_number': form.data['phone_number']}
            return render(request , 'user_signup_form.html', content)

            
    form = forms.phoneNumberForm()
    content = {"form":form}
    return render(request , 'user_signup_form.html', content)
            

def signin_profile_view(request):
    return HttpResponse("signin my profile")


def change_profile_view(request):
    return HttpResponse("change my profile")


def show_profile_view(request, profile_username):
    return HttpResponse(profile_username)
