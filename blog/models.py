from django.db import models
from django.conf import settings
from django.db.models import Manager
from django.utils import timezone

class News(models.Model):
    news_id = models.CharField(max_length=4)
    author = models.CharField(max_length=50)
    author_cid = models.CharField(max_length=8)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    objects = Manager()
    
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
    frequency = models.IntegerField(null=True)


class PilotConnection(Member):
    origin = models.CharField(max_length=4, default="-")
    destination = models.CharField(max_length=4, default="-")

class Staff(Member):
    position = models.CharField(max_length=42, default="-")
    email = models.EmailField()

class Event(models.Model):
    id = models.IntegerField(primary_key=True, default=None)
    title = models.CharField(max_length=42)
    banner = models.ImageField(upload_to="img", null=True)
    event_date = models.DateTimeField(blank=True, null=True)
    # published_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    active = True
    objects = Manager()
    def __str__(self):
        return self.title