from django import forms

from .models import (
    Ngo, ProjectType, Project, Donation
)


class NGOForm(forms.ModelForm):
    class Meta:
        model = Ngo
        fields = '__all__'


class ProjectTypeForm(forms.ModelForm):
    class Meta:
        model = ProjectType
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'
