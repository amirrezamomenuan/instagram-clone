from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from accounts.models import User, Profile
from .models import Message, Chat
from django.db.models import Q
from .forms import MessageForm

def chat_home_view(request):
    username = request.user.username
    chats = Chat.objects.all().filter(Q(sender__user = request.user) | Q(recipient__user = request.user))

    return render(request, "chat_home.html", {'chats':chats, 'username':username})

def chat_conversation_view(request, other_side_username):
    print('stage 1')
    recipient = Profile.objects.get(user__username = other_side_username)
    print(recipient.user.username)
    print(request.user.username)
    try:
        chat = Chat.objects.get(recipient = recipient, sender = request.user.profile)
        print('chat is :' ,chat)
        print('condition 11111111111111111111111')
    except:
        chat = Chat.objects.get_or_create(recipient = request.user.profile, sender = recipient)
        chat = chat[0]
        print('chat is :' ,chat)
        print('condition 222222222222222222222222')

    if request.method =='POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.on_chat = chat
            form.status = request.user == chat.sender.user
            form.save()
            
    if Message.objects.filter(on_chat = chat.id).exists():
        messages = chat.messages.all()
        print('stage 4')
    else:
        messages = []
        print('stage 5')
    print(messages)
        
    
    form = MessageForm()
    return render(request, 'chat_page.html', {'form':form, 'messages':messages, 'username':request.user.username,'other_username':other_side_username})