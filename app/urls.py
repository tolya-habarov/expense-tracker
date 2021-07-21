from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('transactions/', views.TransactionsView.as_view(), name='transactions'),
    path('transactions/add/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('transactions/<int:pk>/', views.EditTransactionView.as_view(), name='edit_transaction'),
]
