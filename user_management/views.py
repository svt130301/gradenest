from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile
from accounts.forms import UserForm, UserProfileForm
from .forms import (
    UserRegistrationForm,
    StudentRegistrationForm,
    StaffRegistrationForm
)
from user_management.models import Student, Staff
from program_management.models import Department


# ---------- STUDENT REGISTRATION ----------
def student_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            # Create user account
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create student profile
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            messages.success(request, "Student registered successfully!")
            return redirect('user_management:user_list')
    else:
        user_form = UserRegistrationForm()
        student_form = StudentRegistrationForm()

    return render(request, 'user_management/student_register.html', {
        'user_form': user_form,
        'student_form': student_form,
    })


# ---------- STAFF REGISTRATION ----------
def staff_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        staff_form = StaffRegistrationForm(request.POST, request.FILES)

        if user_form.is_valid() and staff_form.is_valid():
            # Save user first
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create staff object
            staff = staff_form.save(commit=False)
            staff.user = user

            # Explicitly clear program/department if Office Staff
            if staff_form.cleaned_data.get('role') == 'OfficeStaff':
                staff.program = None
                staff.department = None

            staff.save()

            # Update linked UserProfile
            profile = user.userprofile
            profile.role = staff_form.cleaned_data.get('role')
            profile.save()

            messages.success(request, "Staff registered successfully!")
            return redirect('user_management:user_list')
    else:
        user_form = UserRegistrationForm()
        staff_form = StaffRegistrationForm()

    return render(request, 'user_management/staff_register.html', {
        'user_form': user_form,
        'staff_form': staff_form,
    })


# ---------- ADMIN USER MANAGEMENT ----------
@login_required
def user_list(request):
    users = User.objects.all().order_by('id')
    return render(request, 'user_management/user_list.html', {'users': users})


@login_required
def add_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, "User added successfully.")
            return redirect('user_management:user_list')
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'user_management/user_form.html', {
        'form': user_form,
        'profile_form': profile_form,
        'form_title': 'Add New User'
    })


@login_required
def delete_user(request, user_id):
    """Delete user and related profile"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('user_management:user_list')

    return render(request, 'user_management/user_confirm_delete.html', {'user': user})


@login_required
def add_user_choice(request):
    """Select user type before registration"""
    if request.method == "POST":
        user_type = request.POST.get("user_type")
        if user_type == "student":
            return redirect("user_management:student_register")
        elif user_type == "staff":
            return redirect("user_management:staff_register")
    return render(request, "user_management/add_user_choice.html")


# ---------- EDIT USER ----------
from django import forms

class UserEditForm(forms.ModelForm):
    """Simplified user edit form without password fields"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Detect if Student or Staff
    student = Student.objects.filter(user=user).first()
    staff = Staff.objects.filter(user=user).first()

    if student:
        profile = student
        profile_form_class = StudentRegistrationForm
        template_name = "user_management/student_edit.html"
    elif staff:
        profile = staff
        profile_form_class = StaffRegistrationForm
        template_name = "user_management/staff_edit.html"
    else:
        messages.error(request, "This user does not have a linked profile.")
        return redirect("user_management:user_list")

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, instance=user)
        profile_form = profile_form_class(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            updated_profile = profile_form.save(commit=False)

            # Handle Office Staff edge case (no program/department)
            role = profile_form.cleaned_data.get("role")
            if role == "OfficeStaff":
                updated_profile.program = None
                updated_profile.department = None

            updated_profile.save()

            # Sync UserProfile role
            user.userprofile.role = role
            user.userprofile.save()

            messages.success(request, "User updated successfully.")
            return redirect("user_management:user_list")

    else:
        user_form = UserRegistrationForm(instance=user)
        profile_form = profile_form_class(instance=profile)

    return render(request, template_name, {
        "user_form": user_form,
        "profile_form": profile_form,
        "form_title": "Edit User",
    })


# ---------- MAKE / REMOVE HOD ----------
@require_POST
def make_hod(request, user_id):
    """Toggle HOD status for a teacher and update department."""
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    staff = get_object_or_404(Staff, user=user_profile.user)

    if not staff.department:
        messages.error(request, "Staff does not belong to any department.")
        return redirect('user_management:user_list')

    department = staff.department

    if user_profile.is_hod:
        # Remove HOD
        user_profile.is_hod = False
        if department.hod == user_profile:
            department.hod = None
            department.save()
        messages.info(request, f"{user_profile.user.username} is no longer an HOD.")
    else:
        # Replace existing HOD if exists
        if department.hod and department.hod != user_profile:
            old_hod = department.hod.user.username
            department.hod.is_hod = False
            department.hod.save()
            messages.warning(request, f"Previous HOD ({old_hod}) was replaced.")

        # Assign new HOD
        user_profile.is_hod = True
        department.hod = user_profile
        department.save()
        messages.success(request, f"{user_profile.user.username} is now marked as HOD.")

    user_profile.save()
    return redirect('user_management:user_list')

