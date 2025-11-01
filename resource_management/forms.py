from django import forms
from .models import QuestionPaper, TimeTable

class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['title', 'subject', 'semester', 'file']

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['title', 'program', 'semester', 'exam_type', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if file.content_type != 'application/pdf':
                raise forms.ValidationError("Invalid file type. Please upload a valid PDF.")
        return file

