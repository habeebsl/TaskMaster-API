from django.contrib import admin
from .models import TaskModel, SubTaskModel, CollaboratorModel

# Register your models here.

admin.site.register(TaskModel)
admin.site.register(SubTaskModel)
admin.site.register(CollaboratorModel)
