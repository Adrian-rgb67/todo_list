from django.db import models
from django.contrib.auth.models import User, Group


class Task(models.Model):
    """A creative todo task model with priority, categories, due dates, and user/group assignment."""

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('shopping', 'Shopping'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('finance', 'Finance'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    due_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_tasks', help_text='User who created this task'
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_tasks', help_text='User assigned to this task'
    )
    assigned_group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_tasks', help_text='Group assigned to this task'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def priority_color(self):
        colors = {
            'low': 'green',
            'medium': 'yellow',
            'high': 'red',
        }
        return colors.get(self.priority, 'gray')

    @property
    def category_emoji(self):
        emojis = {
            'personal': '🏠',
            'work': '💼',
            'shopping': '🛒',
            'health': '❤️',
            'education': '📚',
            'finance': '💰',
            'other': '📌',
        }
        return emojis.get(self.category, '📌')

    @property
    def assigned_display(self):
        """Return a human-readable assignment string."""
        parts = []
        if self.assigned_to:
            parts.append(self.assigned_to.get_full_name() or self.assigned_to.username)
        if self.assigned_group:
            parts.append(self.assigned_group.name)
        if parts:
            return ' / '.join(parts)
        return 'Unassigned'
