import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView
from src.accounts.decorators import customer_required
from src.portals.admins.models import Donation, Project


@method_decorator(customer_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'customer/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['donations_count'] = Donation.objects.filter(user=self.request.user).count()
        context['donations_amount_count'] = Donation.objects.filter(user=self.request.user,
                                                                    is_completed=True).aggregate(Sum('amount'))
        context['donations_projects'] = Donation.objects.filter(user=self.request.user, is_completed=True).count()
        context['donations_pending'] = Donation.objects.filter(user=self.request.user, is_completed=False).count()
        return context


@method_decorator(customer_required, name='dispatch')
class NewsFeedView(TemplateView):
    template_name = 'customer/news-feed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeedView, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(is_completed=False)
        return context


@method_decorator(customer_required, name='dispatch')
class DonationListView(ListView):
    queryset = Donation.objects.all()
    template_name = 'customer/donation_list.html'

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user)


class DonateForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['payment_method', 'amount']


stripe.api_key = 'sk_test_51LC794Js59MkLRK8jKm97MecFP4dwcOrxfetIXefvByCaodNGQ1qNdKqaxVBZGD1aW9VTBh69W73T1Ox7LtByRpy00nRXonBff '


@method_decorator(login_required, name='dispatch')
class DonationCreateView(View):

    def get(self, request, pk):
        if request.user.is_superuser or request.user.is_staff:
            messages.warning(request, "Admins are not allowed to donate.")
            return redirect('admins:dashboard')

        project = get_object_or_404(Project.objects.all(), pk=self.kwargs['pk'])
        return render(request, 'customer/donation_form.html', context={'form': DonateForm()})

    def post(self, request, pk):
        form = DonateForm(request.POST)
        project = get_object_or_404(Project.objects.all(), pk=self.kwargs['pk'])

        amount = self.request.POST.get('amount')
        payment_method = self.request.POST.get('payment_method')
        amount_calculation = int(project.donation_amount)+int(amount)
        if amount_calculation <= int(project.required_amount):
            total_amount = int(amount) * 100
            host = self.request.get_host()
            customer = stripe.Customer.create(
                name=self.request.user.username,
                email=self.request.user.email
            )
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer=customer,
                submit_type='pay',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': total_amount,
                            'product_data': {
                                'name': project.name,
                            },
                        },
                        'quantity': 1,
                    },
                ],

                mode='payment',
                success_url='http://' + host + reverse('customer-portal:success') \
                            + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='http://{}{}'.format(host, reverse(
                    'customer-portal:cancel')),
            )
            print(checkout_session['payment_intent'])
            donate = Donation(
                user=self.request.user,
                project=project,
                amount=amount,
                payment_method=payment_method,
                transaction_id=checkout_session['payment_intent'],
                stripe_id=checkout_session['id'],
            )

            donate.save()
            return redirect(checkout_session.url, code=303)
        else:
            max_amount = int(project.required_amount) - int(project.donation_amount)
            messages.error(request, f"Your Maximum Donation Limit is {max_amount}$")
            return redirect('customer-portal:donate',pk)

class SuccessPayment(View):
    def get(self, request, *args, **kwargs):
        stripe_id = self.request.GET.get('session_id')

        donation = Donation.objects.get(user=self.request.user, stripe_id=stripe_id)
        donation.is_paid = True
        donation.save()
        context = {
            'invoice': donation
        }
        return render(self.request, 'customer/success.html', context)


class CancelPayment(TemplateView):
    template_name = 'customer/cancel.html'
