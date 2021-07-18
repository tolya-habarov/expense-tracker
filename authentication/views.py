from typing import Any
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.http import HttpRequest, HttpResponse

from authentication.forms import SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        response = super().post(request, *args, **kwargs)
        if self.object is not User:
            login(request, self.object)
        
        return response
