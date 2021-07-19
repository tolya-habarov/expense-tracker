from django.contrib import admin

from app import models

@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Payee)
class PayeeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass