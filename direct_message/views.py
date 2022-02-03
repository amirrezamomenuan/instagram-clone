from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from accounts.models import User, Profile
from .models import Message, Chat
from django.db.models import Q
from .forms import MessageForm

def chat_home_view(request):
    username = request.user.username
    chats = Chat.objects.all().filter(Q(sender__user = request.user) | Q(recipient__user = request.user))

    return render(request, "chat_home.html", {'chats':chats, 'username':username})

def chat_conversation_view(request, chat_id, other_side_username):
    print('stage 1')
    recipient = Profile.objects.get(user__username = other_side_username)
    print(chat_id)
    if chat_id == 0:
        chat = Chat(sender = request.user.profile, recipient = recipient)
        chat.save()
        print("stage 2")
    else:
        chat = get_object_or_404(Chat, id = chat_id)
        print('stage 3')
    

    if request.method =='POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.on_chat = chat
            form.status = request.user == chat.sender.user
            form.save()
            
    if Message.objects.filter(on_chat = chat).exists():
        messages = chat.messages.all()
        print('stage 4')
    else:
        messages = []
        print('stage 5')
    print(messages)
        
    
    form = MessageForm()
    return render(request, 'chat_page.html', {'form':form, 'messages':messages, 'username':request.user.username,'other_username':other_side_username,'chats_id':chat_id})