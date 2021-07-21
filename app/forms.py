from django import forms
from django.utils import timezone

from app import models


class BaseTransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = '__all__'
        labels = {'transaction_type': 'Type'}
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class AddTransactionForm(BaseTransactionForm):
    def __init__(self, *args, **kwargs):  # type: ignore
        if hasattr(self.Meta, 'initial'):
            initial = kwargs.get('initial', {})
            initial.update(self.Meta.initial)
            kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    class Meta(BaseTransactionForm.Meta):
        initial = {'date': timezone.now()}
