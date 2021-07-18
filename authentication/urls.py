from django.urls import path
from django.contrib.auth import views as auth_views

from authentication import views
from authentication import forms

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(form_class=forms.LoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
]
