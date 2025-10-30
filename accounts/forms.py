from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Program, Subject, FacultyAssignment


# --- User Creation / Edit Form ---
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


# --- User Profile Form (updated to match your current model) ---
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'program', 'phone_number', 'photo', 'identification_document']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'identification_document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# --- Program Form ---
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'code', 'duration']


# --- Subject Form ---
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['program', 'name', 'code', 'semester', 'has_lab']


# --- Faculty Assignment Form ---
class FacultyAssignmentForm(forms.ModelForm):
    class Meta:
        model = FacultyAssignment
        fields = ['teacher', 'subject']

