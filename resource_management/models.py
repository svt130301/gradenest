from django.db import models
from django.contrib.auth.models import User
from program_management.models import Program, Subject


# ------------------------------
# Question Paper (Teacher / HOD)
# ------------------------------
class QuestionPaper(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('SERIES', 'Series Exam'),
        ('MODEL', 'Model Exam'),
        ('UNIVERSITY', 'University Exam'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'userprofile__role__in': ['Teacher', 'HOD']}
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    file = models.FileField(upload_to='resources/question_papers/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.subject.name} (Sem {self.semester})"


# ------------------------------
# Time Table (Office Staff)
# ------------------------------
class TimeTable(models.Model):
    EXAM_TYPE_CHOICES = [
        ('SERIES', 'Series Exam'),
        ('MODEL', 'Model Exam'),
        ('UNIVERSITY', 'University Exam'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'userprofile__role': 'OfficeStaff'}
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.PositiveIntegerField()
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    file = models.FileField(upload_to='resources/timetables/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.program.name} Sem {self.semester}"


# ------------------------------
# Resource Notification (for student pop-up)
# ------------------------------
class ResourceNotification(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ('QUESTION_PAPER', 'Question Paper'),
        ('TIMETABLE', 'Time Table'),
    ]

    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    message = models.CharField(max_length=255)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_resource_type_display()} - {self.message[:40]}"

