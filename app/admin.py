from django.contrib import admin
from .models import AIModel, Project, Run

# Register your models here.
admin.site.register(AIModel)
admin.site.register(Project)
admin.site.register(Run)
