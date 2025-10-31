from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from user_management.models import Student
from program_management.models import Program
from .models import UserProfile, Subject, FacultyAssignment

# -------------------------------
# LOGIN / LOGOUT / HOME
# -------------------------------
def home(request):
    return render(request, 'accounts/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------------
# DASHBOARD
# -------------------------------
@login_required
def dashboard(request):
    user_profile = getattr(request.user, "userprofile", None)
    role = user_profile.role if user_profile else "Unknown"

    context = {
        "user": request.user,
        "role": role,
    }

    # OFFICE STAFF DASHBOARD
    if role == "OfficeStaff":
        from program_management.models import Program, Department
        from user_management.models import Student

        departments = Department.objects.all()
        programs = Program.objects.all()
        selected_program_id = request.GET.get("program")
        selected_semester = request.GET.get("semester")

        students = Student.objects.select_related("program__department")

        if selected_program_id:
            students = students.filter(program_id=selected_program_id)
        if selected_semester:
            students = students.filter(semester=selected_semester)

        context.update({
            "departments": departments,
            "programs": programs,
            "students": students,
            "selected_program_id": int(selected_program_id) if selected_program_id else None,
            "selected_semester": selected_semester,
        })
        return render(request, "accounts/office_dashboard.html", context)


    # -------------------------------
    # HOD DASHBOARD
    # -------------------------------
    elif user_profile and getattr(user_profile, "is_hod", False):
        from program_management.models import Department
        from user_management.models import Staff

        department = Department.objects.filter(hod=user_profile).first()
        teachers = Staff.objects.filter(department=department)

        context.update({
            "department": department.name if department else "Not Assigned",
            "teachers": teachers,
        })
        return render(request, "accounts/hod_dashboard.html", context)

    # -------------------------------
    # TEACHER DASHBOARD
    # -------------------------------
    elif role == "Teacher":
        return render(request, "accounts/teacher_dashboard.html", context)

    # -------------------------------
    # ADMIN DASHBOARD
    # -------------------------------
    elif role == "Admin":
        return render(request, "accounts/admin_dashboard.html", context)

    # -------------------------------
    # STUDENT DASHBOARD
    # -------------------------------
    else:
        return render(request, "accounts/student_dashboard.html", context)


# -------------------------------
# PROGRAM MANAGEMENT (Admin)
# -------------------------------
@login_required
def program_list(request):
    programs = Program.objects.all()
    return render(request, 'accounts/program_list.html', {'programs': programs})


@login_required
def add_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program added successfully.')
            return redirect('program_list')
    else:
        form = ProgramForm()
    return render(request, 'accounts/add_program.html', {'form': form})


@login_required
def delete_program(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    program.delete()
    messages.success(request, 'Program deleted successfully.')
    return redirect('program_list')


# -------------------------------
# SUBJECT MANAGEMENT (Admin)
# -------------------------------
@login_required
def subject_list(request):
    subjects = Subject.objects.select_related('program')
    return render(request, 'accounts/subject_list.html', {'subjects': subjects})


@login_required
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'accounts/add_subject.html', {'form': form})


@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, 'Subject deleted successfully.')
    return redirect('subject_list')


# -------------------------------
# FACULTY ASSIGNMENT (HOD only)
# -------------------------------
@login_required
def assign_faculty(request):
    """Allow HODs to assign teachers to subjects"""
    user_profile = request.user.userprofile

    # Ensure only HODs can access this
    if not getattr(user_profile, "is_hod", False):
        messages.error(request, "Access denied. Only HODs can assign faculty.")
        return redirect('dashboard')

    program = user_profile.program

    # Ensure valid program reference
    if not isinstance(program, Program):
        try:
            program = Program.objects.get(name=program)
        except Program.DoesNotExist:
            messages.error(request, "Invalid program linked to your HOD profile.")
            return redirect('dashboard')

    subjects = Subject.objects.filter(program=program).order_by('semester', 'code')
    teachers = UserProfile.objects.filter(role='Teacher', program=program)

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        teacher_id = request.POST.get('teacher_id')

        if subject_id and teacher_id:
            subject = get_object_or_404(Subject, id=subject_id)
            teacher = get_object_or_404(UserProfile, id=teacher_id)

            FacultyAssignment.objects.update_or_create(
                subject=subject,
                defaults={'teacher': teacher}
            )

            messages.success(request, f"{teacher.user.first_name} assigned to {subject.name}.")
            return redirect('assign_faculty')

    return render(request, 'accounts/assign_faculty.html', {
        'program': program,
        'subjects': subjects,
        'teachers': teachers,
    })

