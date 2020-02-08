from django.shortcuts import render
from .models import Post, Event, PilotConnection, ATCConnection, Member
from django.utils import timezone
import json, urllib

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    events = Event.objects.filter(event_date__gte=timezone.now()).order_by('event_date')
    openurl = urllib.request.urlopen('http://eu.data.vatsim.net/vatsim-data.json')
    if(openurl.getcode() == 200):
        data = openurl.read()
        vatsim_datafeed = json.loads(data)
        pilots = vatsim_datafeed['pilots']
        atc = vatsim_datafeed['controllers']
        online_pilots = []
        online_atc = []
        for i in pilots:
            if( "EG" in i['plan']['departure'] or "EG" in i['plan']['arrival']):
                p = PilotConnection()
                p.cid = i['member']['cid']
                p.name = i['member']['name']
                p.departure = i['plan']['departure']
                p.arrival = i['plan']['arrival']
                p.callsign = i['callsign']
                online_pilots.append(p)
        for i in atc:
            if( "EG" in i['callsign'] ):
                a = ATCConnection()
                a.cid = i['member']['cid']
                a.name = i['member']['name']
                a.callsign = i['callsign']
                a.frequency = i['frequency']
                online_atc.append(a)
    else:
        print('Error loading from JSON datafeed')

    return render(request, 'blog/post_list.html', {'events': events, 'posts': posts, 'online_pilots': online_pilots, 'online_atc': online_atc})