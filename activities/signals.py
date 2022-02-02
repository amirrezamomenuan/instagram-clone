from django.shortcuts import get_object_or_404
from django.db.models import Q


from django.dispatch import receiver
from .models import Activity
from accounts.models import Profile, User
from direct_message.models import Message
from post.models import Comment, Like



from django.db.models.signals import post_save, m2m_changed


@receiver(post_save, sender = Like)
def liked_post_signal(sender, instance, created, **kwargs):
    if created:
        profile = get_object_or_404(Profile, user = instance.on_post.owner.user)
        liker_username = get_object_or_404(User, username = instance.owner.user.username)
        liker_username = liker_username.username

        message_text = f"{liker_username} liked your post"
        Activity.objects.create(related_to = profile, message = message_text)


@receiver(post_save, sender = Comment)
def wrote_comment_on_post(sender, instance, created, **kwargs):
    if created:
        profile = get_object_or_404(Profile, user = instance.on_post.owner.user)
        comment_writer = get_object_or_404(User, username = instance.writer.user.username)
        comment_writer = comment_writer.username

        message_text = f"{comment_writer} wrote a comment on your post"
        Activity.objects.create(related_to = profile, message= message_text)


@receiver(post_save, sender = Message)
def recieved_a_message(sender, instance, created, **kwargs):
    if instance.status:
        profile = Profile.objects.get(Q(user = instance.on_chat.recipient.user))
        message_sender = User.objects.get(Q(username = instance.on_chat.sender.user.username))
    else:
        profile = Profile.objects.get(Q(user = instance.on_chat.sender.user))
        message_sender = User.objects.get(Q(username = instance.on_chat.recipient.user.username))
    message_sender_username = message_sender.username

    message_text = f"{message_sender_username} sent you a new message"
    Activity.objects.create(related_to = profile, message= message_text)


@receiver(m2m_changed, sender = Profile.followers.through)
def followed_you(sender, instance, action, reverse, model, **kwargs):

    #sender is Profile, instance is a profile object , reverse is false, model is User
    if action == "post_add":
        pkeys = kwargs.get('pk_set')
        sender_username = list(pkeys)[0]
        reciever_username = instance.user.username
        reciever_profile = Profile.objects.get(user__username = reciever_username)

        message_text = f"{sender_username} started following you"
        Activity.objects.create(related_to = reciever_profile, message = message_text)
