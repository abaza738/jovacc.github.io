from django.shortcuts import render
from .models import News, Event, PilotConnection, ATCConnection, Member, Staff
from django.utils import timezone
import json, urllib.request, re, datetime

def home(request):
    news_req = urllib.request.Request('http://hq.vatme.net/api/news/vacc/OJAC', headers={'User-Agent': 'Mozilla/5.0'})
    events_req = urllib.request.Request('http://hq.vatme.net/api/events/vacc/OJAC', headers={'User-Agent': 'Mozilla/5.0'})
    events_html = urllib.request.urlopen(events_req).read()
    news_html = urllib.request.urlopen(news_req).read()
    events_list = json.loads(events_html)
    news_list = json.loads(news_html)
    events = []
    news = []
    i = 3
    while(i > 0):
        e = Event()
        e.id = events_list[i]['id']
        e.title = events_list[i]['name']
        e.banner = events_list[i]['bannerLink']
        e.description = events_list[i]['description']
        events.append(e)
        i -= 1
    for k in range(3):
        n = News()
        n.news_id = news_list[k]['id']
        n.title = news_list[k]['title']
        author_cid = news_list[k]['createdBy']
        author_url = "http://hq.vatme.net/api/member/get/"+author_cid
        author_req = urllib.request.Request(author_url, headers={'User-Agent': 'Mozilla/5.0'})
        author_html = urllib.request.urlopen(author_req).read()
        author_dict = json.loads(author_html)
        n.author = author_dict['firstname']+" "+author_dict['lastname']
        n.created_date = news_list[k]['timestamp']['date'].split('.000000')[0]
        n.text = news_list[k]['news']
        news.append(n)
    
    connections_url = urllib.request.urlopen('http://eu.data.vatsim.net/vatsim-data.json')
    if(connections_url.getcode() == 200):
        data = connections_url.read()
        vatsim_datafeed = json.loads(data)
        pilots = []
        atc = []
        online_pilots = []
        online_atc = []
        for i in vatsim_datafeed:
            if( i.clienttype.toUpper() == "PILOT" ):
                pilots.append(i)
            elif( i.clienttype.toUpper() == "ATC" ):
                atc.append(i)
        for i in pilots:
            if( re.match(r"^OJ[A-Z]{2}$", i['planned_depairport']) or re.match(r"^OJ[A-Z]{2}$", i['planned_destairport'])):
                p = PilotConnection()
                p.cid = i['cid']
                p.name = i['realname']
                p.departure = i['planned_depairport']
                p.arrival = i['planned_destairport']
                p.callsign = i['callsign']
                online_pilots.append(p)
        for i in atc:
            if( re.match(r"(^OJ[A-Z]{2}|^AMM_)", i['callsign'])):
                a = ATCConnection()
                a.cid = i['cid']
                a.name = i['realname']
                a.callsign = i['callsign']
                a.frequency = (i['frequency']+100000)/1000
                online_atc.append(a)
    else:
        print('Error loading from JSON datafeed')

    return render(request, 'blog/home.html', {'events': events, 'news': news, 'online_pilots': online_pilots, 'online_atc': online_atc})

def staff(request):
    req = urllib.request.Request('http://hq.vatme.net/api/vacc/staff/OJAC', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    main_list = json.loads(html)
    staff_list = []
    for guy in main_list:
        s = Staff()
        s.name = guy['firstname'] + " " + guy['lastname']
        s.cid = guy['vatsimid']
        s.position = guy['staffposition']
        s.email = guy['email']
        staff_list.append(s)
    return render(request, 'staff/staff.html', {'staff_list': staff_list})

def events(request):
    events_req = urllib.request.Request('http://hq.vatme.net/api/events/vacc/OJAC', headers={'User-Agent': 'Mozilla/5.0'})
    events_html = urllib.request.urlopen(events_req).read()
    events_list = json.loads(events_html)
    events = []
    for i in events_list:
        if (datetime.datetime.now().timestamp() < int(i['datetime'])):
            e = Event()
            e.id = i['id']
            e.title = i['name']
            date = datetime.datetime.fromtimestamp(int(i['datetime']))
            e.event_date = datetime.datetime.strftime(date, "%A, %B %d %Y at %H%Mz")
            e.banner = i['bannerLink']
            e.description = i['description']
            events.append(e)
        else: break
    return render(request, 'events/events.html', {'events': events})

def news(request):
    news_req = urllib.request.Request('http://hq.vatme.net/api/news/vacc/OJAC', headers={'User-Agent': 'Mozilla/5.0'})
    news_html = urllib.request.urlopen(news_req).read()
    news_list = json.loads(news_html)
    news = []
    for news_item in news_list:
        n = News()
        n.news_id = news_item['id']
        n.title = news_item['title']
        author_cid = news_item['createdBy']
        author_url = "http://hq.vatme.net/api/member/get/"+author_cid
        author_req = urllib.request.Request(author_url, headers={'User-Agent': 'Mozilla/5.0'})
        author_html = urllib.request.urlopen(author_req).read()
        author_dict = json.loads(author_html)
        n.author = author_dict['firstname']+" "+author_dict['lastname']
        n.created_date = news_item['timestamp']['date'].split('.000000')[0]
        n.text = news_item['news']
        news.append(n)
    return render(request, 'news/news.html', {'news': news})