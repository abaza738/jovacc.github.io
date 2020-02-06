from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title

class Member(models.Model):
    cid = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=80)
    def __str__(self):
        return self.cid

class ATCConnection(models.Model):
    callsign = models.CharField(max_length=40)
    name = models.ForeignKey(Member, on_delete=models.CASCADE)
    rating = models.IntegerField()
    def __str__(self):
        return self.callsign

class PilotConnection(models.Model):
    callsign = models.CharField(max_length=40)
    name = models.ForeignKey(Member, on_delete=models.CASCADE)
    altitude = models.IntegerField()
    origin = models.CharField(max_length=4, default="-")
    destination = models.CharField(max_length=4, default="-")
    def __str__(self):
        return self.callsign

