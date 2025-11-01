from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from program_management.models import Program, Subject
from user_management.models import Student
from .models import ExternalSubjectMark


@login_required
def enter_external_marks(request):
    """
    View for Office Staff to manually enter external marks of students.
    Allows filtering by Program and Semester.
    """

    # Check access role
    if not hasattr(request.user, "userprofile") or request.user.userprofile.role != "OfficeStaff":
        messages.error(request, "Only Office Staff can access this page.")
        return redirect("home")

    # Dropdown filters
    programs = Program.objects.all()
    selected_program = request.GET.get("program")
    selected_semester = request.GET.get("semester")

    students = []
    subjects = []

    # Filter based on selected program and semester
    if selected_program and selected_semester:
        students = Student.objects.filter(
            program_id=selected_program,
            current_semester=selected_semester
        ).order_by("user__first_name")

        subjects = Subject.objects.filter(
            program_id=selected_program,
            semester=selected_semester
        ).order_by("subject_code")

    # Handle form submission
    if request.method == "POST" and students and subjects:
        for student in students:
            for subject in subjects:
                mark_key = f"{student.id}_{subject.id}"
                marks = request.POST.get(mark_key)
                if marks:
                    ExternalSubjectMark.objects.update_or_create(
                        student=student,
                        subject=subject,
                        defaults={"marks": marks}
                    )
        messages.success(request, "Marks saved successfully.")
        return redirect("enter_external_marks")

    context = {
        "programs": programs,
        "students": students,
        "subjects": subjects,
        "selected_program": selected_program,
        "selected_semester": selected_semester,
    }

    return render(request, "marks_management/enter_external_marks.html", context)

