from django import forms
from django.contrib.auth.models import User
from .models import Student, Staff
from program_management.models import Program, Department


# ------------------ USER REGISTRATION FORM ------------------
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


# ------------------ STUDENT REGISTRATION FORM ------------------
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'program', 'semester', 'admission_number', 'roll_number', 'admission_year',
            'dob', 'blood_group', 'phone',
            'father_name', 'mother_name', 'guardian_name',
            'guardian_number', 'guardian_email', 'address',
            'pin_code', 'photo', 'identification_document',
            'tenth_percentage', 'twelfth_percentage', 'bachelor_percentage'
        ]

        widgets = {
            'program': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'admission_number': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_number': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'identification_document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tenth_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'twelfth_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'bachelor_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tenth = cleaned_data.get('tenth_percentage')
        twelfth = cleaned_data.get('twelfth_percentage')
        bachelor = cleaned_data.get('bachelor_percentage')

        # Logic for which fields are required
        if bachelor:  # Master’s student (has bachelor marks)
            if not (tenth and twelfth):
                raise forms.ValidationError("Master’s students must provide 10th, 12th, and Bachelor’s percentages.")
        else:  # Bachelor’s student
            if not (tenth and twelfth):
                raise forms.ValidationError("Bachelor’s students must provide 10th and 12th percentages.")

        return cleaned_data


# ------------------ STAFF REGISTRATION FORM ------------------
from django import forms
from .models import Staff

class StaffRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Teacher', 'Teacher'),
        ('OfficeStaff', 'Office Staff'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Staff
        fields = [
            'role', 'staff_id', 'program', 'department', 'designation',
            'qualification', 'experience_years',
            'phone', 'address', 'date_of_birth', 'gender', 'blood_type',
            'educational_qualification', 'identification_document', 'photo'
        ]

        widgets = {
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'educational_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'identification_document': forms.FileInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """Ensure program and department are not required for Office Staff."""
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'OfficeStaff':
            # Remove program and department for office staff
            cleaned_data['program'] = None
            cleaned_data['department'] = None
        return cleaned_data

