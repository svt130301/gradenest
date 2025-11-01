# marks_management/utils.py
from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum, F
from program_management.models import Subject
from .models import ExternalSubjectMark, ExternalSemesterResult
from django.shortcuts import get_object_or_404

# Grade mapping: percentage -> (grade, grade_point)
GRADE_MAP = [
    (85, ("O", Decimal("10"))),
    (75, ("A", Decimal("9"))),
    (60, ("B", Decimal("8"))),
    (50, ("C", Decimal("7"))),
    (40, ("D", Decimal("6"))),
    (0,  ("F", Decimal("0"))),
]


def percent_to_grade_and_gp(percent: Decimal):
    """Return (grade_str, grade_point Decimal) for a percent (0-100)."""
    for threshold, (grade, gp) in GRADE_MAP:
        if percent >= Decimal(threshold):
            return grade, gp
    return "F", Decimal("0")


def quantize(value):
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def calculate_semester_result(student, program, semester, exam_type=None, admission_year=None, entered_by=None):
    """
    Calculate and save ExternalSemesterResult for one student + semester.
    - Aggregates ExternalSubjectMark for the given (student, exam_semester, exam_type).
    - Uses Subject.external_marks as the subject's max external mark if available,
      otherwise assumes 100.
    - Computes total_marks, percentage, overall_grade, sgpa (weighted by credits), cgpa (avg sgpa across available semesters).
    Returns the ExternalSemesterResult instance.
    """
    # Filter marks for this student/semester (and exam_type if provided)
    marks_qs = ExternalSubjectMark.objects.filter(
        student=student,
        exam_semester=semester,
    )
    if exam_type:
        marks_qs = marks_qs.filter(exam_type=exam_type)
    if admission_year:
        marks_qs = marks_qs.filter(admission_year=admission_year)

    # If no subject marks, create or update a "empty" semester result (or skip)
    if not marks_qs.exists():
        return None

    # We'll compute:
    # - subject_totals: sum of marks_obtained
    # - subject_max_total: sum of subject.external_marks (or 100 fallback)
    # - weighted grade points for SGPA (subject credits * grade_point)
    total_obtained = Decimal("0")
    total_max = Decimal("0")
    total_weighted_gp = Decimal("0")
    total_credits = Decimal("0")

    # iterate marks and lookup subject credits & external max
    for mark in marks_qs.select_related("subject"):
        if mark.marks_obtained is None:
            continue
        # convert Decimal to Decimal safely
        mark_val = Decimal(mark.marks_obtained)
        subj = mark.subject

        # determine max marks for external component
        try:
            subj_max = Decimal(subj.external_marks) if getattr(subj, "external_marks", None) is not None else Decimal("100")
        except Exception:
            subj_max = Decimal("100")
        # Determine total max marks for this subject (external + internal if available)
        try:
            total_subj_max = Decimal("0")

            # include external marks if field exists
            if hasattr(subj, "external_marks") and subj.external_marks:
                total_subj_max += Decimal(subj.external_marks)

            # include internal marks if field exists
            if hasattr(subj, "internal_marks") and subj.internal_marks:
                total_subj_max += Decimal(subj.internal_marks)

            # fallback default if neither present
            if total_subj_max == 0:
                total_subj_max = Decimal("100")

        except Exception:
            total_subj_max = Decimal("100")

        subj_max = total_subj_max

        # determine credit weight
        credits = Decimal(getattr(subj, "credits", 0) or 0)

        total_obtained += mark_val
        total_max += subj_max

        # subject percentage (0-100)
        # Normalize marks_obtained to percentage based on subject.external_marks (not total)
        try:
            ext_max = Decimal(subj.external_marks) if getattr(subj, "external_marks", None) else Decimal("100")
        except Exception:
            ext_max = Decimal("100")

        # Convert obtained marks to percentage
        subj_percent = (mark_val / ext_max * Decimal("100")) if ext_max > 0 else Decimal("0")
        subj_percent = quantize(subj_percent)

        # Determine grade and grade point based on percentage
        grade_str, gp = percent_to_grade_and_gp(subj_percent)


        total_weighted_gp += gp * credits
        total_credits += credits

    # avoid divide by zero
    percentage = (total_obtained / total_max * Decimal("100")) if total_max > 0 else Decimal("0")
    percentage = quantize(percentage)

    # overall grade by percentage
    overall_grade, _ = percent_to_grade_and_gp(percentage)

    # SGPA: weighted average grade point across subjects (by credits)
    sgpa = (total_weighted_gp / total_credits) if total_credits > 0 else Decimal("0")
    sgpa = quantize(sgpa)

    # CGPA: average of sgpa across all existing ExternalSemesterResult records for this student (including this semester)
    # We'll upsert this semester result first (without cgpa), then compute cgpa
    result_defaults = {
        "program": program,
        "exam_semester": semester,
        "admission_year": admission_year,
        "exam_type": exam_type or ExternalSubjectMark.objects.filter(student=student, exam_semester=semester).first().exam_type,
        "total_marks": quantize(total_obtained),
        "percentage": percentage,
        "sgpa": sgpa,
        "overall_grade": overall_grade,
        "pass_fail": "Pass" if percentage >= Decimal("40") else "Fail",  # pass threshold 40%
    }
    if entered_by:
        result_defaults["entered_by"] = entered_by

    sem_result, created = ExternalSemesterResult.objects.update_or_create(
        student=student,
        exam_semester=semester,
        exam_type=result_defaults["exam_type"],
        defaults=result_defaults,
    )

    # Now compute CGPA across all semesters (for same program & admission_year & exam_type)
    qs = ExternalSemesterResult.objects.filter(student=student)
    if admission_year:
        qs = qs.filter(admission_year=admission_year)
    # include all exam types? use same exam_type to be consistent
    qs = qs.filter(exam_type=sem_result.exam_type)

    # compute average of sgpa (ignore null)
    sgpa_agg = qs.aggregate(total_sgpa=Sum("sgpa"), count_sgpa=Sum(models.Case(models.When(sgpa__isnull=False, then=1), default=0)))
    total_sgpa = sgpa_agg["total_sgpa"] or Decimal("0")
    count_sgpa = sgpa_agg["count_sgpa"] or 0
    if count_sgpa and count_sgpa > 0:
        cgpa = Decimal(total_sgpa) / Decimal(count_sgpa)
    else:
        cgpa = sgpa

    sem_result.cgpa = quantize(Decimal(cgpa))
    sem_result.save()

    return sem_result

