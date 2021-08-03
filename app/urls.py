from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='home'),
    path('transactions/', views.CurrentDateTransactionsView.as_view(), name='transactions'),
    path('transactions/<int:year>/<int:month>/', views.TransactionsView.as_view(), name='month_transactions'),
    path('transactions/add/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('transactions/edit/<int:pk>/', views.EditTransactionView.as_view(), name='edit_transaction'),

    path('accounts/add', views.AddAccountView.as_view(), name='add_account'),
    path('accounts/edit/<int:pk>/', views.EditAccountView.as_view(), name='edit_account'),
]
