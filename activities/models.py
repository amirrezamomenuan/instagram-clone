from django.db import models
from accounts.models import Profile

class Activity(models.Model):

    related_to = models.ForeignKey(Profile, on_delete= models.CASCADE)
    message = models.CharField(max_length=60)
    seen = models.BooleanField(default=False)
    datetime = models.DateTimeField(null=True, auto_now_add=True)

    class Meta:
        ordering = ['-datetime',]
        

    def __str__(self):
        return self.message[:30]+ '...' if len(self.message) > 30 else self.message

    def change_to_seen(self):
        self.seen = True
        self.save()
        