from django.contrib import admin
from .models import (
    ProjectType, Donation, Ngo, Project
)

admin.site.register(Ngo)
admin.site.register(ProjectType)
admin.site.register(Project)
admin.site.register(Donation)
