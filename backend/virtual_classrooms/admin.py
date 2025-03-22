from django.contrib import admin
from .models import VirtualClassroom

@admin.register(VirtualClassroom)
class VirtualClassroomAdmin(admin.ModelAdmin):
    list_display = ("title", "host", "platform", "start_time", "duration")
