from django.contrib import admin
from .models import Post,Comment,Like, Reply,CommentLike

admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CommentLike)