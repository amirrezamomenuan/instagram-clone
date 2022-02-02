from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from accounts.models import User, Profile
from .models import Message, Chat
from django.db.models import Q
from .forms import MessageForm

def chat_home_view(request):
    username = request.user.username
    chats = Chat.objects.all().filter(Q(sender__user = request.user) | Q(recipient__user = request.user))

    return render(request, "chat_home.html", {'chats':chats, 'username':username})

def chat_conversation_view(request, chat_id):
    chat = get_object_or_404(Chat, id = chat_id)
    messages = chat.messages.all()
    if request.method =='POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.on_chat = chat
            form.status = request.user == chat.sender.user
            form.save()
    
    form = MessageForm()
    return render(request, 'chat_page.html', {'form':form, 'messages':messages, 'username':request.user.username})