# marks_management/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone

# Use strings in ForeignKey to avoid import-time/circular issues
# 'user_management.Student' and 'program_management.Subject' exist in your project

class ExamType(models.TextChoices):
    REGULAR = 'REG', 'Regular'
    IMPROVEMENT = 'IMP', 'Improvement'
    SUPPLEMENTARY = 'SUP', 'Supplementary'

class ExternalSubjectMark(models.Model):
    # use string app_label.ModelName to avoid import errors
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE, related_name='external_subject_marks')
    subject = models.ForeignKey('program_management.Subject', on_delete=models.CASCADE, related_name='external_subject_marks')
    program = models.ForeignKey('program_management.Program', on_delete=models.SET_NULL, null=True, blank=True)
    exam_semester = models.PositiveIntegerField()  # the semester this exam belongs to
    admission_year = models.PositiveIntegerField(null=True, blank=True)  # denormalized for quick filtering
    exam_type = models.CharField(max_length=3, choices=ExamType.choices, default=ExamType.REGULAR)
    marks_obtained = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    grade = models.CharField(max_length=8, blank=True, null=True)
    passed = models.BooleanField(default=False)
    pass_fail = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], blank=True, null=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='entered_external_marks')
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ensure only one record per student-subject-semester-exam_type
        unique_together = ('student', 'subject', 'exam_semester', 'exam_type')
        indexes = [
            models.Index(fields=['program', 'exam_semester', 'admission_year']),
        ]
        ordering = ['student', 'subject']

    def can_edit(self, user=None):
        """Regular results locked; Improvements/Supplementary editable."""
        return self.exam_type in (ExamType.IMPROVEMENT, ExamType.SUPPLEMENTARY)

    def __str__(self):
        student_str = getattr(self.student, 'admission_number', str(self.student))
        subj_name = getattr(self.subject, 'name', str(self.subject))
        return f"{student_str} - {subj_name} - S{self.exam_semester} - {self.get_exam_type_display()}"

class ExternalSemesterResult(models.Model):
    student = models.ForeignKey('user_management.Student', on_delete=models.CASCADE, related_name='external_semester_results')
    program = models.ForeignKey('program_management.Program', on_delete=models.SET_NULL, null=True, blank=True)
    exam_semester = models.PositiveIntegerField()
    admission_year = models.PositiveIntegerField(null=True, blank=True)
    exam_type = models.CharField(max_length=3, choices=ExamType.choices, default=ExamType.REGULAR)
    total_marks = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    sgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    overall_grade = models.CharField(max_length=8, blank=True, null=True)
    pass_fail = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')], blank=True, null=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='entered_external_semester_results')
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'exam_semester', 'exam_type')
        indexes = [
            models.Index(fields=['program', 'exam_semester', 'admission_year']),
        ]
        ordering = ['student', 'exam_semester']

    def can_edit(self, user=None):
        return self.exam_type in (ExamType.IMPROVEMENT, ExamType.SUPPLEMENTARY)

    def __str__(self):
        student_str = getattr(self.student, 'admission_number', str(self.student))
        return f"{student_str} - S{self.exam_semester} - {self.get_exam_type_display()}"

