from django import forms
from .models import QuestionPaper, TimeTable

class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['title', 'subject', 'semester', 'file']

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['title', 'program', 'semester', 'file']

