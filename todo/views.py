from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Task
from .forms import TaskForm, TaskEditForm


class TaskListView(ListView):
    """Display all tasks with filtering and search capabilities."""
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
        context['current_search'] = self.request.GET.get('search', '')
        return context


class TaskCreateView(CreateView):
    """Create a new task."""
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Task created successfully! Time to get things done.')
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
        messages.success(self.request, 'Task deleted. Sometimes less is more!')
        return super().form_valid(form)


def toggle_task(request, pk):
    """Toggle a task's completed status."""
    task = get_object_or_404(Task, pk=pk)
    task.completed = not task.completed
    task.save()
    if task.completed:
        messages.success(request, f'Nice work! "{task.title}" marked as complete!')
    else:
        messages.info(request, f'"{task.title}" moved back to active tasks.')
    return redirect('task-list')


def clear_completed(request):
    """Delete all completed tasks at once."""
    completed = Task.objects.filter(completed=True)
    count = completed.count()
    if count > 0:
        completed.delete()
        messages.success(request, f'{count} completed task{"s" if count > 1 else ""} cleared! Fresh start.')
    else:
        messages.info(request, 'No completed tasks to clear.')
    return redirect('task-list')
