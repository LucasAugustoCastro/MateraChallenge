from django.contrib import admin
from .models import User, Loan, Payment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("user","description","nominal_value","interest_rate","ip_address","bank", "created_at", "updated_at")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("loan","value","payed_at", "created_at", "updated_at")
