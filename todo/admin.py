from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from .models import Task
from .resources import TaskResource


@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    resource_class = TaskResource
    list_display = ('title', 'completed', 'priority', 'category', 'assigned_to', 'assigned_group', 'due_date', 'created_at')
    list_filter = ('completed', 'priority', 'category', 'assigned_group', 'assigned_to')
    search_fields = ('title', 'description')
    list_editable = ('completed', 'priority')
    ordering = ('-created_at',)


# Keep default User and Group admin but ensure they're registered
if not admin.site.is_registered(User):
    admin.site.register(User, UserAdmin)

if not admin.site.is_registered(Group):
    admin.site.register(Group, GroupAdmin)
