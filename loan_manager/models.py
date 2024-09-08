import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True

class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)


class Loan(Base):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, related_name='loans', on_delete=models.CASCADE)
    description = models.TextField(blank=True, default='')
    nominal_value = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    ip_address = models.CharField(max_length=45)
    bank = models.CharField(max_length=255)
    request_date = models.DateField()
    
    class Meta():
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    def __str__(self):
        return f'Emprestimo no valor de {self.nominal_value} com o banco {self.bank}'

    def get_debt_balance(self):
        total_paid = self.payments.aggregate(models.Sum('value'))['value__sum'] or 0
        debt_balance = self.nominal_value + (self.nominal_value * self.interest_rate / 100) - total_paid
        return max(debt_balance, 0)

class Payment(Base):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    loan = models.ForeignKey(Loan, related_name='payments', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    payed_at = models.DateTimeField()

    class Meta():
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f'Pagamento do emprestimo {self.loan.id} no valor de {self.value}'