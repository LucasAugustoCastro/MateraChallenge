from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
    
class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, ip_address=self.request.META.get('REMOTE_ADDR'))

    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        loan = self.get_object()
        payments = loan.payments.all()
        if not payments:
            return Response({"message": "No register payments"})
        serializer = PaymentSerializer(loan.payments.all(), many=True)
        return Response(serializer.data)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(loan__user=user)
