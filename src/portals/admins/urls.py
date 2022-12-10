from django.urls import path, include
from django.views.generic import TemplateView
from .views import *

app_name = "admins"
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('ngo/<int:pk>/change/', NGOUpdateView.as_view(), name='ngo-update'),

    path('projecttype/', ProjectTypeListView.as_view(), name='projecttype-list'),
    path('projecttype/add/', ProjectTypeCreateView.as_view(), name='projecttype-create'),
    path('projecttype/<int:pk>/change/', ProjectTypeUpdateView.as_view(), name='projecttype-update'),
    path('projecttype/<int:pk>/delete/', ProjectTypeDeleteView.as_view(), name='projecttype-delete'),

    path('project/', ProjectListView.as_view(), name='project-list'),
    path('project/add/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/change/', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),

    path('donation/', DonationListView.as_view(), name='donation-list'),
    path('donation/<int:pk>/change/', DonationUpdateView.as_view(), name='donation-update'),
    path('donation/<int:pk>/delete/', DonationDeleteView.as_view(), name='donation-delete'),

    path('payment/verification/easypaisa/', PaymentVerificationEasyPaisa.as_view(), name='payment-verification-easypaisa')

]
