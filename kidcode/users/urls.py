from django.urls import path, re_path, register_converter
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('password-change/', views.UserPasswordChange.as_view(), name="password_change"),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
         name="password_change_done"),
    path('register/', views.RegisterUser.as_view(), name='register'),
    
]