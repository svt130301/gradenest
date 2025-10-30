from django import forms
from .models import Program, Subject


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['department', 'name', 'num_years', 'num_semesters', 'description']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'num_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_semesters': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }



class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            'program', 'code', 'name', 'semester', 'course_type',
            'credits', 'lecture_hours', 'practical_hours',
            'tutorial_hours','integrated_lab', 'internal_marks', 
            'external_marks',
            'is_project', 'is_viva'
        ]

        widgets = {
            'program': forms.Select(attrs={'class': 'form-select'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'course_type': forms.Select(attrs={'class': 'form-select'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'lecture_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'practical_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'tutorial_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'internal_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'external_marks': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'integrated_lab': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_project': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_viva': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

