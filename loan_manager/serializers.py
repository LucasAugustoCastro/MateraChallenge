from rest_framework import serializers
from .models import User, Loan, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'loan',
            'value',
            'payed_at',
            'created_at',
            'updated_at',
            'deleted',
        )
class LoanSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    ip_address = serializers.IPAddressField(read_only=True)
    debt_balance = serializers.SerializerMethodField()
    class Meta:
        model = Loan
        fields = (
            'id',
            'description',
            'nominal_value',
            'interest_rate',
            'ip_address',
            'bank',
            'created_at',
            'updated_at',
            'deleted',
            'debt_balance',
            'payments',
            'request_date'
        )
        
    def get_debt_balance(self, obj:Loan):
        return obj.get_debt_balance()

