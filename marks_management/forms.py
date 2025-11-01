from django import forms
from .models import ExternalSubjectMark
from program_management.models import Subject

class ExternalMarksEntryForm(forms.ModelForm):
    class Meta:
        model = ExternalSubjectMark
        fields = ['student', 'subject', 'marks_obtained', 'pass_fail']
        widgets = {
            'student': forms.HiddenInput(),
            'subject': forms.HiddenInput(),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'placeholder': 'Enter marks'
            }),
            'pass_fail': forms.Select(choices=[('Pass', 'Pass'), ('Fail', 'Fail')], attrs={
                'class': 'form-select'
            }),
        }

class SemesterSelectionForm(forms.Form):
    program = forms.ModelChoiceField(
        queryset=None,
        label="Select Program",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    semester = forms.ChoiceField(
        choices=[],
        label="Select Semester",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    academic_year = forms.CharField(
        required=False,
        label="Admission Year (Optional)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2024-2026'})
    )

    def __init__(self, *args, **kwargs):
        from program_management.models import Program
        super().__init__(*args, **kwargs)
        self.fields['program'].queryset = Program.objects.all()
        self.fields['semester'].choices = [(i, f'Semester {i}') for i in range(1, 7)]

