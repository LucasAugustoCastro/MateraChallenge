from .views import LoanViewSet, PaymentViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('loans', LoanViewSet, basename='loan')
router.register('payment', PaymentViewSet, basename='payment')
