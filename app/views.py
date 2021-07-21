from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from app import models
from app import forms


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'page-blank.html')


class TransactionsView(LoginRequiredMixin, ListView):
    template_name = 'transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self) -> QuerySet[models.Transaction]:
        return models.Transaction.objects.filter(account__user=self.request.user)


class AddTransactionView(LoginRequiredMixin, CreateView):
    form_class = forms.AddTransactionForm
    template_name = 'add_transaction.html'
    success_url = reverse_lazy('transactions')
