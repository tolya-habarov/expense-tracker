from decimal import Decimal

from django import forms
from django.utils import timezone

from app import models
from app import services


def validate_date(date):
    if date > timezone.now().date():
        raise forms.ValidationError(
            'The date cannot be in the future!',
            params={'date': date},
        )

    return date


class AddTransactionForm(forms.Form):
    name = forms.CharField(max_length=100)
    date = forms.DateField(
        initial=timezone.now(),
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[validate_date],
    )
    amount = forms.DecimalField(
        min_value=Decimal('.00'),
        initial=Decimal('.00'),
        max_digits=10,
        decimal_places=2,
    )
    notes = forms.CharField(
        widget=forms.Textarea(),
        required=False,
    )
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

        self.cleaned_data['transaction_type'] = int(self.cleaned_data['transaction_type'])

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

        transaction = models.Transaction(**self.cleaned_data)
        services.add_transaction(transaction)
        return transaction


class EditTransactionForm(forms.ModelForm):
    date = forms.DateField(
        initial=timezone.now(),
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[validate_date],
    )

    class Meta:
        model = models.Transaction
        fields = '__all__'
        labels = {'transaction_type': 'Type'}
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '0'}),
        }


class AddAccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  # type: ignore
        if hasattr(self.Meta, 'initial'):
            initial = kwargs.get('initial', {})
            initial.update(self.Meta.initial)
            kwargs['initial'] = initial

        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Account
        fields = '__all__'
        exclude = ['user']
        widgets = {'balance': forms.NumberInput(attrs={'min': '0'})}
        initial = {'balance': Decimal('.00')}


class EditAccountForm(forms.ModelForm):
    class Meta(AddAccountForm.Meta):
        initial = {}  # type: ignore
