from dateutil.relativedelta import relativedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Loan, Payment, User

class LoanTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.authentication()
        self.loan = Loan.objects.create(
            description = "teste",
            nominal_value = 1000,
            interest_rate = 5,
            ip_address = '127.0.0.1',
            bank = 'Banco XYZ',
            request_date = '2024-07-07',
            user=self.user
        )
        
    def authentication(self):
        url = reverse('token_obtain_pair')  # Endpoint para obter o token
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        # Definir o token de acesso no cabeçalho de autorização
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")



    def test_create_loan(self):
        url = reverse('loan-list')
        data = {
            'nominal_value': 1500,
            'interest_rate': 6,
            'ip_address': '127.0.0.1',
            'bank': 'Banco ABC',
            'request_date': '2024-07-01',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 2)

    def test_view_loan(self):
        url = reverse('loan-detail', args=[self.loan.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nominal_value'], '1000.00')

    def test_debt_balance(self):
        Payment.objects.create(
            loan=self.loan, 
            value=200,
            payed_at = '2024-07-08'
            )
        url = reverse('loan-detail', args=[self.loan.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['debt_balance']), 1000 + 1000 * 5 / 100 - 200)

    def test_create_payment(self):
        url = reverse('payment-list')
        data = {
            'loan': self.loan.id,
            'value': 100,
            'payed_at': '2024-07-08'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get(id=response.data['id']).value, 100)

    def test_view_payment(self):
        payment = Payment.objects.create(
            loan = self.loan,
            value = '30',
            payed_at = '2024-07-08'
        )
        url = reverse('payment-detail', args=[payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], '30.00')
    
    def test_view_payments_from_loan(self):
        from datetime import date
        for i in range(5):
            payment_date = date(2024,7,8)
            Payment.objects.create(
                loan = self.loan,
                value = '30',
                payed_at =str(payment_date + relativedelta(months=i))
            )

        url = reverse('loan-payments', args=[self.loan.id])
        response = self.client.get(url)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['value'], '30.00')
        self.assertEqual(response.data[0]['payed_at'], '2024-07-08T00:00:00Z')

    def test_view_payments_from_loan_withou_payment(self):
        url = reverse('loan-payments', args=[self.loan.id])
        response = self.client.get(url)
        self.assertEqual(response.data['message'], 'No register payments')
