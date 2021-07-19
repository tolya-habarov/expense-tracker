from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('transactions/', views.TransactionsView.as_view(), name='transactions'),
]
