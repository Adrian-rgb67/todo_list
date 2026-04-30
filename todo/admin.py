from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'priority', 'category', 'due_date', 'created_at')
    list_filter = ('completed', 'priority', 'category')
    search_fields = ('title', 'description')
    list_editable = ('completed', 'priority')
    ordering = ('-created_at',)
