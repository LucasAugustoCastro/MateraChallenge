from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
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



# class UsersAPIView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
# class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    

# class LoansAPIView(generics.ListCreateAPIView):
#     queryset = Loan.objects.all()
#     serializer_class = LoanSerializer

#     def get_queryset(self):
#         print("aaaaaaaa")
#         user_id = self.kwargs.get('user_pk')
#         if user_id:
#             return self.queryset.filter(user_id = user_id )
        
#         return self.queryset.all()

# class LoanAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Loan.objects.all()
#     serializer_class = LoanSerializer
#     def get_object(self):
#         user_id = self.kwargs.get('user_pk')
#         if user_id:
#             return get_object_or_404(self.get_queryset(), user_id = user_id, pk=self.kwargs.get('loan_pk'))
#         return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('loan_pk'))


# class LoanAPIView(APIView):
#     def get(self, request):
#         loans = Loan.objects.all()
#         serializer = LoanSerializer(loans, many=True)
#         return Response(serializer.data)
# class PaymentAPIView(APIView):
#     def get(self, request):
#         payments = Payment.objects.all()
#         serializer = PaymentSerializer(payments, many=True)
#         return Response(serializer.data)