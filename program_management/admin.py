from django.contrib import admin
from .models import Program, Subject, FacultyAssignment
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hod")
    search_fields = ("name",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("name", "num_years", "num_semesters", "description")
    search_fields = ("name",)
    list_filter = ("num_years", "num_semesters")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "code", "name", "program", "semester",
        "course_type", "credits",
        "lecture_hours", "practical_hours",
        "integrated_lab",
        "internal_marks", "external_marks", "total_marks",
        "is_project", "is_viva",
    )
    list_filter = (
        "program", "semester", "course_type",
        "integrated_lab", "is_project", "is_viva",
    )
    search_fields = ("code", "name", "program__name")
    ordering = ("program", "semester", "code")

    def save_model(self, request, obj, form, change):
        obj.total_marks = obj.internal_marks + obj.external_marks
        super().save_model(request, obj, form, change)


@admin.register(FacultyAssignment)
class FacultyAssignmentAdmin(admin.ModelAdmin):
    list_display = ("subject", "teacher", "assigned_by", "assigned_at")
    search_fields = ("subject__name", "teacher__username", "assigned_by__username")
    list_filter = ("assigned_at",)

