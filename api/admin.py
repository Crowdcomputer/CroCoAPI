# Register your models here.
from django.contrib import admin
from api.models import CrowdUser, App, Task, Task, TaskInstance

admin.site.register(CrowdUser)
admin.site.register(App)
admin.site.register(Task)
admin.site.register(TaskInstance)