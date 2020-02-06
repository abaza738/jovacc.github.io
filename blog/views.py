from django.shortcuts import render
from .models import Post, Event
from django.utils import timezone

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def events_list(request):
    events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')
    return render(request, 'blog/post_list.html', {'events': events})