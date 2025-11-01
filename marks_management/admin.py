from django.contrib import admin
from .models import ExternalSubjectMark, ExternalSemesterResult

@admin.register(ExternalSubjectMark)
class ExternalSubjectMarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'program', 'exam_semester', 'exam_type', 'marks_obtained', 'grade', 'pass_fail')
    list_filter = ('program', 'exam_semester', 'exam_type', 'pass_fail')
    search_fields = ('student__user__username', 'student__admission_number', 'subject__name')
    autocomplete_fields = ('student', 'subject', 'program')
    ordering = ('student', 'subject')

@admin.register(ExternalSemesterResult)
class ExternalSemesterResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'program', 'exam_semester', 'exam_type', 'total_marks', 'percentage', 'sgpa', 'cgpa', 'overall_grade', 'pass_fail')
    list_filter = ('program', 'exam_semester', 'exam_type', 'pass_fail')
    search_fields = ('student__user__username', 'student__admission_number')
    ordering = ('student', 'exam_semester')

