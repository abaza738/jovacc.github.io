from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name="post_list"),
    path('staff', views.staff, name="staff"),
    path('events', views.events, name="events"),
    path('news', views.news, name="news")
]