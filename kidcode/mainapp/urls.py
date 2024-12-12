from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='home'),
    path('constructor/', views.FieldsSettings.as_view(), name='constructor'),
    path('profile/', views.UserPasswordChange.as_view(), name = 'profile'),
    path('journal/', views.Journal.as_view(), name='journal'),
    path('record/', views.record, name='record'),
    path('task/<int:pk>/', views.Task.as_view(), name='task'),
    path('update_grade/', views.update_grade, name='update_grade'),
]