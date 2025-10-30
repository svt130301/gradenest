from django import forms
from .models import Program, Subject


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'duration', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program Name'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 Years'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description...'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['program', 'code', 'name', 'semester', 'has_lab']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-select'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., MCA101'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1'}),
            'has_lab': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
