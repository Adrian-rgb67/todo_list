from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponse
from import_export.formats.base_formats import DEFAULT_FORMATS
from .models import Task
from .forms import TaskForm, TaskEditForm, TaskImportForm
from .resources import TaskResource


def _sidebar_categories():
    """Return sidebar category data: (slug, label, emoji, count)."""
    categories = []
    for slug, label in Task.CATEGORY_CHOICES:
        emojis = {
            'personal': '🏠', 'work': '💼', 'shopping': '🛒',
            'health': '❤️', 'education': '📚', 'finance': '💰', 'other': '📌',
        }
        count = Task.objects.filter(category=slug).count()
        categories.append((slug, label, emojis.get(slug, '📌'), count))
    return categories


def _sidebar_groups():
    """Return sidebar group data: (id, name, task_count)."""
    groups = []
    for group in Group.objects.all().order_by('name'):
        count = Task.objects.filter(assigned_group=group).count()
        groups.append((group.id, group.name, count))
    return groups


class TaskListView(ListView):
    """Display all tasks with filtering, search, and group/user capabilities."""
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all()
        # Filter by status
        status = self.request.GET.get('status', 'all')
        if status == 'active':
            queryset = queryset.filter(completed=False)
        elif status == 'completed':
            queryset = queryset.filter(completed=True)
        # Filter by priority
        priority = self.request.GET.get('priority', 'all')
        if priority != 'all':
            queryset = queryset.filter(priority=priority)
        # Filter by category
        category = self.request.GET.get('category', 'all')
        if category != 'all':
            queryset = queryset.filter(category=category)
        # Filter by assigned group
        group = self.request.GET.get('group', 'all')
        if group != 'all':
            queryset = queryset.filter(assigned_group_id=group)
        # Filter by assigned user
        assigned = self.request.GET.get('assigned', 'all')
        if assigned != 'all':
            queryset = queryset.filter(assigned_to_id=assigned)
        # Search by title
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.count()
        context['completed_tasks'] = Task.objects.filter(completed=True).count()
        context['active_tasks'] = Task.objects.filter(completed=False).count()
        context['high_priority_tasks'] = Task.objects.filter(priority='high', completed=False).count()
        # Progress percentage
        if context['total_tasks'] > 0:
            context['progress'] = int((context['completed_tasks'] / context['total_tasks']) * 100)
        else:
            context['progress'] = 0
        # Current filters
        context['current_status'] = self.request.GET.get('status', 'all')
        context['current_priority'] = self.request.GET.get('priority', 'all')
        context['current_category'] = self.request.GET.get('category', 'all')
        context['current_group'] = self.request.GET.get('group', 'all')
        context['current_assigned'] = self.request.GET.get('assigned', 'all')
        context['current_search'] = self.request.GET.get('search', '')
        # Sidebar data
        context['categories_sidebar'] = _sidebar_categories()
        context['groups_sidebar'] = _sidebar_groups()
        # Groups and users for filter dropdowns
        context['all_groups'] = Group.objects.all().order_by('name')
        from django.contrib.auth.models import User
        context['all_users'] = User.objects.all().order_by('username')
        return context


class TaskCreateView(CreateView):
    """Create a new task."""
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'

    def form_valid(self, form):
        # Auto-set created_by to current user if authenticated
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        messages.success(self.request, 'Task created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-list')


class TaskUpdateView(UpdateView):
    """Update an existing task."""
    model = Task
    form_class = TaskEditForm
    template_name = 'todo/task_edit.html'

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    """Delete a task."""
    model = Task
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        messages.success(self.request, 'Task deleted!')
        return super().form_valid(form)


def toggle_task(request, pk):
    """Toggle a task's completed status."""
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    if task.completed:
        messages.success(request, f'Nice work! "{task.title}" completed!')
    else:
        messages.info(request, f'"{task.title}" moved back to active.')
    return redirect('task-list')


def clear_completed(request):
    """Delete all completed tasks at once."""
    completed = Task.objects.filter(completed=True)
    count = completed.count()
    if count > 0:
        completed.delete()
        messages.success(request, f'{count} completed task{"s" if count > 1 else ""} cleared!')
    else:
        messages.info(request, 'No completed tasks to clear.')
    return redirect('task-list')


# ===== IMPORT / EXPORT VIEWS =====

def export_tasks(request):
    """Export tasks to CSV, JSON, or XLSX."""
    file_format = request.GET.get('format', 'csv')
    resource = TaskResource()

    # Apply same filters as list view
    queryset = Task.objects.all()
    status = request.GET.get('status', 'all')
    if status == 'active':
        queryset = queryset.filter(completed=False)
    elif status == 'completed':
        queryset = queryset.filter(completed=True)
    group = request.GET.get('group', 'all')
    if group != 'all':
        queryset = queryset.filter(assigned_group_id=group)
    category = request.GET.get('category', 'all')
    if category != 'all':
        queryset = queryset.filter(category=category)

    dataset = resource.export(queryset)

    format_map = {
        'csv': ('text/csv', 'csv', dataset.csv),
        'json': ('application/json', 'json', dataset.json),
        'xlsx': ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xlsx', dataset.xlsx),
    }

    if file_format not in format_map:
        file_format = 'csv'

    content_type, ext, data = format_map[file_format]
    response = HttpResponse(data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="tasks.{ext}"'
    return response


class TaskImportView(FormView):
    """Import tasks from a file."""
    template_name = 'todo/task_import.html'
    form_class = TaskImportForm
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        import_file = form.cleaned_data['import_file']
        resource = TaskResource()

        # Determine format from file extension
        filename = import_file.name.lower()
        if filename.endswith('.json'):
            file_format = 'json'
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_format = 'xlsx'
        else:
            file_format = 'csv'

        try:
            dataset = resource.import_data(
                {'file_data': import_file.read(), 'format': file_format},
                dry_run=False,
            )
            messages.success(
                self.request,
                f'Import complete! {dataset.totals["new"]} new, '
                f'{dataset.totals["update"]} updated, '
                f'{dataset.totals["delete"]} deleted, '
                f'{dataset.totals["skip"]} skipped.'
            )
        except Exception as e:
            messages.error(self.request, f'Import failed: {str(e)}')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_sidebar'] = _sidebar_categories()
        context['groups_sidebar'] = _sidebar_groups()
        return context
