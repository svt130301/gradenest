from django.contrib import admin
from .models import QuestionPaper, TimeTable, ResourceNotification


@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'program', 'semester', 'uploaded_by', 'uploaded_at')
    list_filter = ('program', 'semester', 'question_type')
    search_fields = ('title', 'uploaded_by__username', 'subject__name')


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'semester', 'exam_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('program', 'semester', 'exam_type')
    search_fields = ('title', 'uploaded_by__username')


@admin.register(ResourceNotification)
class ResourceNotificationAdmin(admin.ModelAdmin):
    list_display = ('resource_type', 'message', 'program', 'semester', 'is_read', 'created_at')
    list_filter = ('resource_type', 'program', 'semester', 'is_read')

