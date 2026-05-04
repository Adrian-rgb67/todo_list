from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.contrib.auth.models import User, Group
from .models import Task


class TaskResource(resources.ModelResource):
    """Import/Export resource for Task model with user-friendly field names."""

    assigned_to_username = fields.Field(
        column_name='assigned_to_username',
        attribute='assigned_to',
        widget=ForeignKeyWidget(User, 'username'),
    )
    assigned_group_name = fields.Field(
        column_name='assigned_group_name',
        attribute='assigned_group',
        widget=ForeignKeyWidget(Group, 'name'),
    )
    created_by_username = fields.Field(
        column_name='created_by_username',
        attribute='created_by',
        widget=ForeignKeyWidget(User, 'username'),
    )

    class Meta:
        model = Task
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('id',)

    def get_export_order(self):
        return (
            'id', 'title', 'description', 'completed', 'priority',
            'category', 'due_date', 'assigned_to_username',
            'assigned_group_name', 'created_by_username',
            'created_at', 'updated_at',
        )
