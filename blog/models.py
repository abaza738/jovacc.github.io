from django.db import models
from django.conf import settings
from django.db.models import Manager
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = Manager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title

class Member(models.Model):
    cid = models.IntegerField(unique=True, null=False)
    name = models.CharField(max_length=80)
    callsign = models.CharField(max_length=40)
    objects = Manager()

    def __str__(self):
        return self.cid+self.callsign

class ATCConnection(Member):
    frequency = models.IntegerField()


class PilotConnection(Member):
    origin = models.CharField(max_length=4, default="-")
    destination = models.CharField(max_length=4, default="-")

class Event(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=42)
    banner = models.ImageField()
    event_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    event_text = models.TextField()
    active = True
    objects = Manager()
    def __str__(self):
        return self.title
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def deactivate(self):
        if self.published_date < timezone.now():
            self.active = False