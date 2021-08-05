from django.urls import path
from django.urls.base import reverse_lazy
from django.views.generic.base import RedirectView

from app import views

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('transactions')), name='home'),

    path('transactions/', views.CurrentDateTransactionsView.as_view(), name='transactions'),
    path('transactions/<int:year>/<int:month>/', views.TransactionsView.as_view(), name='month_transactions'),
    path('transactions/add/', views.AddTransactionView.as_view(), name='add_transaction'),
    path('transactions/edit/<int:pk>/', views.EditTransactionView.as_view(), name='edit_transaction'),

    path('accounts/add', views.AddAccountView.as_view(), name='add_account'),
    path('accounts/edit/<int:pk>/', views.EditAccountView.as_view(), name='edit_account'),
]
