
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    hod = models.ForeignKey(
        'accounts.UserProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        limit_choices_to={'role': 'Teacher', 'is_hod': True},
        related_name='departments_headed'
    )

    def __str__(self):
        return self.name



class Program(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    num_years = models.PositiveIntegerField(default=0)
    num_semesters = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name




class Subject(models.Model):
    COURSE_TYPE_CHOICES = [
        ('CORE', 'Core'),
        ('ELECTIVE', 'Elective'),
        ('LAB', 'Lab'),
        ('PROJECT', 'Project'),
        ('VIVA', 'Comprehensive Viva'),
        ('SEMINAR', 'Seminar'),
        ('AEC', 'AEC'),
        ('MDC', 'MDC'),
        ('DSC', 'DSC'),
        ('BRIDGE', 'Bridge Course'),
    ]

    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    semester = models.PositiveIntegerField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)

    credits = models.PositiveIntegerField()
    lecture_hours = models.PositiveIntegerField(default=0)
    practical_hours = models.PositiveIntegerField(default=0)
    tutorial_hours = models.PositiveIntegerField(default=0)
    integrated_lab = models.BooleanField(default=False)

    internal_marks = models.PositiveIntegerField(default=0)
    external_marks = models.PositiveIntegerField(default=0)
    total_marks = models.PositiveIntegerField(default=0)

    is_project = models.BooleanField(default=False)
    is_viva = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Auto-calculate total marks
        self.total_marks = self.internal_marks + self.external_marks
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"



class FacultyAssignment(models.Model):
    subject = models.ForeignKey('program_management.Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
    	User,
    	on_delete=models.CASCADE,
    	limit_choices_to={'userprofile__role': 'Teacher'}
    )
    assigned_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='assignments_made')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
      #  unique_together = ('subject',)  # if you want only one teacher per subject. Remove if multiple allowed
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.subject.name} → {self.teacher.username}"
