from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from user_management.models import Student
from program_management.models import Program, Subject, FacultyAssignment
from accounts.models import UserProfile
# ---------- Forms ----------
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['department', 'name', 'num_years', 'num_semesters', 'description']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            'program', 'code', 'name', 'semester', 'course_type',
            'credits', 'lecture_hours', 'practical_hours',
            'tutorial_hours','integrated_lab',
            'internal_marks', 'external_marks',
            'is_project', 'is_viva'
        ]

# ---------- Program Views ----------
def program_list(request):
    programs = Program.objects.all().order_by('id')
    return render(request, 'program_management/program_list.html', {'programs': programs})


def program_add(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'program_management/program_form.html', {'form': form, 'form_title': 'Add Program'})


def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('program_list')
    else:
        form = ProgramForm(instance=program)
    return render(request, 'program_management/program_form.html', {'form': form, 'form_title': 'Edit Program'})


def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == 'POST':
        program.delete()
        return redirect('program_list')
    return render(request, 'program_management/program_confirm_delete.html', {'program': program})


# ---------- Subject Views ----------
@login_required
def subject_list(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    subjects = Subject.objects.filter(program=program).order_by('semester', 'code')
    return render(request, 'program_management/subject_list.html', {'subjects': subjects, 'program': program})


@login_required
def subject_add(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.program = program
            subject.save()
            messages.success(request, "Subject added successfully.")
            return redirect('program_management:subject_list', program_id=program.id)
    else:
        form = SubjectForm()
    return render(request, 'program_management/subject_form.html', {'form': form, 'program': program})


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect('program_management:subject_list', program_id=subject.program.id)
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'program_management/subject_form.html', {'form': form, 'program': subject.program})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    program_id = subject.program.id  # store before deleting
    subject.delete()
    messages.success(request, "Subject deleted successfully.")
    return redirect('program_management:subject_list', program_id=program_id)


# ---------- Faculty Assignment ----------
class AssignFacultyForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset = User.objects.filter(userprofile__role='Teacher'),
        required=True,
        label="Assign to Teacher"
    )

    class Meta:
        model = Subject
        fields = ['teacher']


@login_required
def assign_faculty(request, subject_id):
    from accounts.models import UserProfile
    from program_management.models import Subject, FacultyAssignment
    subject = get_object_or_404(Subject, pk=subject_id)
    user_profile = getattr(request.user, "userprofile", None)

    # --- Ensure only HODs can assign ---
    if not user_profile or not getattr(user_profile, "is_hod", False):
        messages.error(request, "Access denied. Only HODs can assign faculty.")
        return redirect('program_management:assign_faculty_dashboard')

    # --- Normalize program reference ---
    hod_program = user_profile.program
    if isinstance(hod_program, str):  # If stored as name instead of FK
        from program_management.models import Program
        try:
            hod_program = Program.objects.get(name=hod_program)
        except Program.DoesNotExist:
            messages.error(request, "Your HOD profile is not linked to a valid program.")
            return redirect('program_management:assign_faculty_dashboard')

    # --- Ensure HOD belongs to the same program ---
    if hod_program != subject.program:
        messages.error(request, "You can only assign faculty for your own department’s subjects.")
        return redirect('program_management:assign_faculty_dashboard')

    # --- List eligible teachers ---
    teachers = UserProfile.objects.filter(role='Teacher', program=hod_program)

    # --- Handle form submission ---
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        teacher = get_object_or_404(UserProfile, id=teacher_id)

        FacultyAssignment.objects.update_or_create(
            subject=subject,
            defaults={'teacher': teacher.user}
        )

        messages.success(request, f"{teacher.user.first_name or teacher.user.username} assigned to {subject.name}.")
        return redirect('program_management:assign_faculty_dashboard')

    # --- Render page ---
    return render(request, 'program_management/assign_faculty.html', {
        'subject': subject,
        'teachers': teachers,
    })




# ---------- Program Students ----------
def program_students(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    students = Student.objects.filter(program=program)
    return render(request, 'program_management/program_students.html', {
        'program': program,
        'students': students
    })

def all_subjects(request):
    subjects = Subject.objects.select_related('program').all()
    return render(request, 'program_management/all_subjects.html', {'subjects': subjects})

@login_required
def assign_faculty_dashboard(request):
    """Faculty assignment dashboard for HODs"""
    subjects = Subject.objects.all().order_by('program', 'semester')
    assignments = FacultyAssignment.objects.select_related('subject', 'teacher', 'teacher__staff_profile')

    # Create mapping {subject_id: teacher_user}
    assignment_map = {a.subject.id: a.teacher for a in assignments}

    return render(request, 'program_management/assign_faculty_dashboard.html', {
        'subjects': subjects,
        'assignment_map': assignment_map,
    })

@login_required
def promote_students(request):
    """Office Staff: Promote all students to next semester (if not final semester)."""
    user_profile = getattr(request.user, "userprofile", None)
    if not user_profile or user_profile.role != "OfficeStaff":
        messages.error(request, "Access denied. Only Office Staff can promote students.")
        return redirect("dashboard")

    students = Student.objects.select_related("program").all()

    if request.method == "POST":
        promoted_count = 0
        for student in students:
            max_semesters = student.program.num_semesters if student.program else 6
            if student.semester < max_semesters:
                student.semester += 1
                student.save()
                promoted_count += 1
        messages.success(request, f"{promoted_count} students have been promoted to the next semester.")
        return redirect("program_management:promote_students")

    return render(request, "program_management/promote_students.html", {
        "students": students,
    })

