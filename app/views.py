from django.shortcuts import render
from django.views.generic import ListView
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from app import models

@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'page-blank.html')


class TransactionsView(LoginRequiredMixin, ListView):
    template_name = 'transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self) -> QuerySet[models.Transaction]:
        return models.Transaction.objects.filter(account__user=self.request.user)
