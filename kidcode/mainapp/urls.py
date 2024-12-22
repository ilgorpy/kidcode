from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='home'),
    path('constructor/', views.FieldsSettings.as_view(), name='constructor'),
    path('profile/', views.UserProfileChangeView.as_view(), name = 'profile'),
    path('chapters/', views.get_chapters, name='chapters'),
    path('levels/<str:chapter_name>/', views.get_levels, name='levels'),
    path('task/<int:pk>', views.Task1.as_view(), name='task'),
    path('task/<int:pk>/data/', views.Task1.as_view(), name='task-data'),
     path('task/<int:pk>/clue/', views.Task1.as_view(), name='task-clue'),
    path('journal/', views.Journal.as_view(), name='journal'),
    path('record/', views.record, name='record'),
    path('update_grade/', views.update_grade, name='update_grade'),
]