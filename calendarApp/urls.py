from django.urls import path
from . import views

urlpatterns = [
    path('google-authenticate/',
         views.google_authenticate,
         name='google_authenticate'),
    path('google-authenticate-callback/',
         views.google_authenticate_callback,
         name='google_authenticate_callback'),
    path('my-calendar/', views.my_calendar_view, name='my_calendar_view'),
    path('', views.authenticate_btn, name='authenticate_btn'),
]
