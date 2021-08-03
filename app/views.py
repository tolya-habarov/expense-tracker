from typing import Any, Dict, Optional

from django.utils import timezone
from django.views.generic.dates import MonthArchiveView
from django.views.generic.base import RedirectView
from django.views.generic.edit import DeletionMixin, FormView, UpdateView
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from app import models
from app import forms
from app import services


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'page-blank.html')


class CurrentDateTransactionsView(LoginRequiredMixin, RedirectView):
    pattern_name = 'month_transactions'

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        now = timezone.now()
        return super().get_redirect_url(*(args + (now.year, now.month)), **kwargs)


class TransactionsView(LoginRequiredMixin, MonthArchiveView):
    template_name = 'transactions/view.html'
    context_object_name = 'transactions'
    date_field = 'date'
    month_format= '%m'
    allow_empty = True

    def get_queryset(self) -> QuerySet[models.Transaction]:
        return models.Transaction.objects.filter(account__user=self.request.user)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['accounts'] = self.request.user.accounts.all()
        return context


class AddTransactionView(LoginRequiredMixin, FormView):
    form_class = forms.AddTransactionForm
    template_name = 'transactions/add.html'
    success_url = reverse_lazy('transactions')

    def form_valid(self, form: forms.AddTransactionForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditTransactionView(LoginRequiredMixin, UpdateView, DeletionMixin):
    form_class = forms.EditTransactionForm
    template_name = 'transactions/edit.html'
    success_url = reverse_lazy('transactions')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if 'delete' in request.POST:
            request = self.delete(request, *args, **kwargs)
        else:
            request =  super().post(request, *args, **kwargs)
        
        services.update_balance(self.object.account)
        return request

    def get_object(self, queryset: Optional[QuerySet] = None) -> models.Transaction:
        return get_object_or_404(
            models.Transaction,
            account__user=self.request.user,
            pk=self.kwargs['pk'],
        )
