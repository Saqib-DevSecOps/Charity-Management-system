from django.db.models import Sum
from django.views.generic import TemplateView, DetailView

from src.accounts.models import User
from src.portals.admins.models import Project


class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all().count()
        context['projects_count'] = Project.objects.all().count()
        context['funds'] = Project.objects.all().aggregate(Sum('donation_amount'))
        context['projects'] = Project.objects.filter(is_completed=False)[:6]
        context['projects_all'] = Project.objects.filter(is_completed=False)
        return context


class ProjectView(DetailView):
    template_name = 'website/project_detail.html'
    queryset = Project.objects.all()
