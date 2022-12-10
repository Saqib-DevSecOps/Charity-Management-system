from django.urls import path
from django.views.generic import TemplateView
from .views import DonationCreateView, DonationListView, DashboardView, SuccessPayment, CancelPayment

app_name = "customer-portal"
urlpatterns = [

    path(
        'dashboard', DashboardView.as_view(), name='dashboard'
    ),
    path('donation/', DonationListView.as_view(), name='donation-list'),
    path('project/<int:pk>/donate/', DonationCreateView.as_view(), name='donate'),
    path('payment-success/',SuccessPayment.as_view(), name="success"),
    path('payment-cancelled/',CancelPayment.as_view(), name="cancel"),

]
