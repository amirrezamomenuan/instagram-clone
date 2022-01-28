from csv import writer
from django.db import models
from accounts.models import User, Profile


class Post(models.Model):
    location_choices = (
        ('th/ir', "Tehran/Iran"),
        ('ta/ir', "Tabriz/Iran"),
        ('ma/us', "Malibu/Usa"),
        ('ny/us', "NewYork/Usa"),
        ('bj/ch', "Beijing/China"),
        ('hk/ch', "Hongkong/China"),
    )


    image = models.ImageField()
    caption = models.TextField(max_length=100)
    location = models.CharField(max_length=5, choices=location_choices, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username


class Comment(models.Model):
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.content[:10]
    

class Like(models.Model):
    on_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    on_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        if not self.on_comment:
            return f'{self.owner.user} liked {self.on_post}'
        return f'{self.owner.user} liked {self.on_comment}'


class Reply(models.Model):
    content = models.CharField(max_length=50)
    on_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:15]
