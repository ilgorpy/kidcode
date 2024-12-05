from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='home'),
    path('constructor/', views.constructor, name='constructor'),
    #path('profile/', views.profile, name='profile'),
    path('profile/', views.UserPasswordChange.as_view(), name = 'profile'),
    path('journal/', views.journal, name='journal'),
    path('record/', views.record, name='record'),
    path('task/', views.task, name='task'),
]