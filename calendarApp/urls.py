from django.urls import path
from . import views

urlpatterns = [
    path('GoogleCalendarInitView/',
         views.GoogleCalendarInitView,
         name='GoogleCalendarInitView'),
    path('GoogleCalendarRedirectView/',
         views.GoogleCalendarRedirectView,
         name='GoogleCalendarRedirectView'),
    path('my-calendar/', views.GoogleCalendarInitView, name='GoogleCalendarInitView'),
    path('', views.authenticate_btn, name='authenticate_btn'),
]
