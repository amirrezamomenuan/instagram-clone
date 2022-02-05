from cProfile import Profile
from django.shortcuts import redirect, render, HttpResponse
from direct_message.models import Chat
from django.db.models import Q

from post.models import Post
from . import models, forms
from .utils import phone_number_validator
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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
            login(request, user)
            return redirect("profile:show", profile_username = username)
        else:
            content = {"form":form, 'phone_number': form.data['phone_number']}
            return render(request , 'user_signup_form.html', content)

            
    form = forms.phoneNumberForm()
    content = {"form":form}
    return render(request , 'user_signup_form.html', content)


# this view is for logging in users that have their passwordand username
def signin_profile_view(request):
    if request.method == 'POST':
        form = forms.signinForm(request.POST)
        if form.is_valid():
            print("signin form is valid")
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user:
                login(request, user)
                return HttpResponse('login succesfull :)')
                
        content = {"form":form, "form_errors":form.errors}
        return render(request , 'user_signin_form.html', content)

    form = forms.signinForm()
    content = {"form":form}
    return render(request , 'user_signin_form.html', content)


@login_required(login_url= 'profile:signin')
def change_profile_view(request):
    if request.method == 'POST':
        instance = get_object_or_404(models.Profile, user = request.user)
        form = forms.changeProfileForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("profile:show", profile_username = request.user.username)
    
    form = forms.changeProfileForm(instance = get_object_or_404(models.Profile, user = request.user))
    return render(request, "change_profile.html", {'form':form})

@login_required(login_url= 'profile:signin')
def show_profile_view(request, profile_username):
    user = get_object_or_404(models.User, username = profile_username)
    profile = get_object_or_404(models.Profile, user = user)
    posts = Post.objects.filter(owner = profile)
    owner = request.user == user
    state = request.user in profile.followers.all()
    if Chat.objects.filter((Q(sender = profile) & Q(recipient = request.user.profile)) | (Q(recipient = profile) & Q(sender = request.user.profile))).exists():
        chat_id = Chat.objects.filter((Q(sender = profile) & Q(recipient = request.user.profile)) | (Q(recipient = profile) & Q(sender = request.user.profile))).first().id
    else:
        chat_id = 0
    return render(request, "show-profile.html", {'user':user, 'profile':profile, 'posts':posts, 'owner':owner, 'following':state, 'chats_id':chat_id})


# this view is for logging in users that have forgotten their password but have account
def forgot_password_view(request):
    print(request.POST)
    if request.POST.get('confirmation_code'):
        print('hi 1')
        form = forms.codeValidationForm(request.POST)
        if form.is_valid():
            print('verification_code is valid')
            verification_code = form.cleaned_data['confirmation_code']
            phone_number = form.data['phone_number']
            print(confirmation_codes)
            if verification_code == str(confirmation_codes[-1][0]):
                print("yes")
                user = models.User.objects.get(phone_number = phone_number)
                login(request, user)
                return redirect("profile:show", profile_username=user.username)

            else:
                print('no')
                content = {'form':form, 'phone_number':phone_number,}
                return render(request, "forgot_password.html", content)
        return HttpResponse(" invalid verification")

    if request.method == "POST" and not request.POST.get('verification_code'):
        print('hi 2')
        form = forms.phoneNumberForm_forgot(request.POST)
        phone_number = ''
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            form = forms.codeValidationForm()
            sms = phone_number_validator(phone_number)
            confirmation_codes.append(sms)
            
        content = {'form':form, 'phone_number':phone_number,}
        return render(request, "forgot_password.html", content)

            

    form = forms.phoneNumberForm_forgot()
    content = {'form':form}
    return render(request, "forgot_password.html", content)


def search_user_view(request):
    if request.method == 'POST':
        given_input = request.POST.get('search')
        profiles = models.Profile.objects.filter(user__username__icontains = given_input)
        return render(request, 'search_results.html', {'profiles':profiles})

def followers_view(request, requested):
    profile = models.Profile.objects.get(user__username = requested)
    group = profile.followers.all()
    return render(request, 'followers.html', {'group':group,'user':profile.user, 'group_name':'followers'})

def following_view(request, requested):
    profile = models.Profile.objects.get(user__username = requested)
    group = models.User.objects.get(username = requested).following.all()
    return render(request, 'following.html', {'group':group,'user':profile.user, 'group_name':'following'})

@login_required(login_url= 'profile:signin')
def follow_manager_view(request):
    username = request.POST.get('follow')
    profile = get_object_or_404(models.Profile, user__username = username)
    user = request.user
    if user.profile != profile:
        if request.user not in profile.followers.all():
            profile.followers.add(request.user)
        else:
            profile.followers.remove(request.user)
        profile.save()

    return redirect("profile:show", profile_username = username)