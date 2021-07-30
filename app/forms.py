from django import forms
from django.utils import timezone

from app import models


class EditTransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = '__all__'
        labels = {'transaction_type': 'Type'}
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class AddTransactionForm(forms.Form):
    name = forms.CharField(max_length=100)
    date = forms.DateField(
        initial=timezone.now(),
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    notes = forms.CharField(widget=forms.Textarea())
    account = forms.ModelChoiceField(queryset=None)
    transaction_type = forms.ChoiceField(
        choices=models.Transaction.Type.choices,
        label='Type',
    )
    category = forms.CharField(max_length=50)
    payee = forms.CharField(max_length=50)

    def __init__(self, user, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['account'].queryset = self.user.accounts.all()

    def save(self) -> models.Transaction:
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate."
                % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )

        category, _ = models.Category.objects.get_or_create(
            user=self.user,
            name=self.cleaned_data['category'],
        )
        self.cleaned_data['category'] = category

        payee, _ = models.Payee.objects.get_or_create(
            user=self.user,
            name=self.cleaned_data['payee'],
        )
        self.cleaned_data['payee'] = payee

        return models.Transaction.objects.create(**self.cleaned_data)
