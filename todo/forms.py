from django import forms
from django.contrib.auth.models import User, Group
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for creating tasks with user/group assignment."""

    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=False,
        empty_label='Unassigned',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
        })
    )

    assigned_group = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by('name'),
        required=False,
        empty_label='No group',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'category', 'due_date', 'assigned_to', 'assigned_group']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 placeholder-gray-400',
                'placeholder': 'What needs to be done?',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 placeholder-gray-400 resize-none',
                'placeholder': 'Add some details (optional)',
                'rows': 3,
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800',
                'type': 'date',
            }),
        }


class TaskEditForm(forms.ModelForm):
    """Form for editing existing tasks with user/group assignment."""

    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=False,
        empty_label='Unassigned',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
        })
    )

    assigned_group = forms.ModelChoiceField(
        queryset=Group.objects.all().order_by('name'),
        required=False,
        empty_label='No group',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'category', 'due_date', 'assigned_to', 'assigned_group', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 resize-none',
                'rows': 3,
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800 bg-white',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent outline-none transition-all text-sm text-gray-800',
                'type': 'date',
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-brand-500 border-gray-300 rounded focus:ring-brand-500 cursor-pointer',
            }),
        }


class TaskImportForm(forms.Form):
    """Form for importing tasks from a file."""
    import_file = forms.FileField(
        label='Select file (CSV, JSON, or XLSX)',
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-brand-50 file:text-brand-600 hover:file:bg-brand-100 cursor-pointer',
            'accept': '.csv,.json,.xlsx,.xls',
        })
    )
