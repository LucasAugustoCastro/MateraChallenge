from rest_framework import serializers
from .models import User, Loan, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        model = User
        fields = (
            'id',
            'name',
            'cpf',
            'email',
            'cep',
            'address',
            'address_number',
            'created_at',
            'updated_at',
            'deleted',
        )

class LoanSerializer(serializers.ModelSerializer):
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
        )

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'value',
            'payed_at',
            'created_at',
            'updated_at',
            'deleted',
        )