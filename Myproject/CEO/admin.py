
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CEO)
admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Message)
admin.site.register(Log)
admin.site.register(Event)


