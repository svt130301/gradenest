from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q

from user_management.models import Student
from program_management.models import Program, Subject
from .models import ExternalSubjectMark, ExternalSemesterResult
from .forms import SemesterSelectionForm
from .utils import calculate_semester_result
from .models import ExamType
#from .decorators import office_staff_required  # adjust import if needed


# ✅ Access control: Only Office Staff or Admins
def office_staff_required(user):
    """Check if logged-in user is Office Staff or Admin"""
    if not user.is_authenticated:
        return False
    try:
        profile = user.userprofile
        return profile.role == "OfficeStaff" or profile.role == "Admin" or user.is_superuser
    except Exception:
        return False


# ✅ Step 1: Select program, semester, and optionally admission year
@login_required
@user_passes_test(office_staff_required)
def select_program_semester(request):
    if request.method == "POST":
        form = SemesterSelectionForm(request.POST)
        if form.is_valid():
            program = form.cleaned_data["program"]
            semester = int(form.cleaned_data["semester"])
            admission_year = form.cleaned_data.get("academic_year")

            # redirect properly using path parameters
            if admission_year:
                return redirect("marks_management:enter_external_marks_year", program_id=program.id, semester=semester, academic_year=admission_year)
            else:
                return redirect("marks_management:enter_external_marks", program_id=program.id, semester=semester)

    else:
        form = SemesterSelectionForm()

    return render(
        request,
        "marks_management/office/select_program_semester.html",
        {"form": form},
    )

# Step 2: Enter and update external marks

@login_required
@user_passes_test(office_staff_required)
def enter_external_marks(request, program_id, semester):
    admission_year = request.GET.get("admission_year")

    program = get_object_or_404(Program, id=program_id)
    subjects = Subject.objects.filter(program=program, semester=semester)

    filters = Q(program=program, semester=semester)
    if admission_year:
        filters &= Q(admission_year=admission_year)
    students = Student.objects.filter(filters).order_by("roll_number", "user__username")

    if request.method == "POST":
        for student in students:
            for subject in subjects:
                marks_field = f"marks_{student.id}_{subject.id}"
                grade_field = f"grade_{student.id}_{subject.id}"
                pass_field = f"pass_{student.id}_{subject.id}"

                marks = request.POST.get(marks_field)
                grade = request.POST.get(grade_field)
                passed = request.POST.get(pass_field) == "on"

                # skip empty marks (you can change and store zero)
                if marks is None or marks == "":
                    continue

                #create/update subject mark record; ensure required fields are set
                exam_type_value = ExamType.REGULAR
                ExternalSubjectMark.objects.update_or_create(
                    student=student,
                    subject=subject,
                    exam_semester=semester,
                    defaults={
                       "program": program,
                       "admission_year": admission_year,
                       "marks_obtained": marks,
                       "grade": grade or "",
                       "passed": True if float(marks) >= 40 else False,  # auto-pass/fail
                       "pass_fail": "Pass" if float(marks) >= 40 else "Fail",
                       "exam_type": exam_type_value,
                       "entered_by": request.user,
                    },
                )

        # After saving all subject marks, compute semester-level results for each student
        for student in students:
            calculate_semester_result(student=student, program=program, semester=semester, exam_type=None, admission_year=admission_year, entered_by=request.user)

        messages.success(request, "External marks updated and semester results generated.")
        return redirect(f"/marks/office/enter/{program_id}/{semester}/" + (f"?admission_year={admission_year}" if admission_year else ""))

    # Preload marks for display
    student_marks = {}
    for student in students:
        student_marks[student.id] = {}
        for subject in subjects:
            mark = ExternalSubjectMark.objects.filter(student=student, subject=subject, exam_semester=semester).first()
            student_marks[student.id][subject.id] = mark

    return render(
        request,
        "marks_management/office/enter_external_marks.html",
        {
            "program": program,
            "semester": semester,
            "admission_year": admission_year,
            "students": students,
            "subjects": subjects,
            "student_marks": student_marks,
        },
    )
    
@login_required
@user_passes_test(office_staff_required)
def view_external_results(request, program_id, semester):
    admission_year = request.GET.get("admission_year")
    program = get_object_or_404(Program, id=program_id)
    qs = ExternalSemesterResult.objects.filter(program=program, exam_semester=semester)
    if admission_year:
        qs = qs.filter(admission_year=admission_year)
    results = qs.select_related("student").order_by("student__roll_number", "student__user__username")
    return render(request, "marks_management/office/view_external_results.html", {
        "program": program,
        "semester": semester,
        "admission_year": admission_year,
        "results": results,
    })

