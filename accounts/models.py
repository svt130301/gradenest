# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Program model (e.g., BCA, MCA)
class Program(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    duration = models.IntegerField(help_text="Duration in years")

    def __str__(self):
        return f"{self.name} ({self.code})"


# Subject model
class Subject(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField()
    has_lab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - Sem {self.semester}"

# User Profile (extends Django User)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('OfficeStaff', 'Office Staff'),
        ('Student', 'Student'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    program = models.ForeignKey('program_management.Program', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    identification_document = models.FileField(upload_to='documents/', null=True, blank=True)
    is_hod = models.BooleanField(default=False)  # used by "Make HOD" button

    def __str__(self):
        return f"{self.user.username} ({self.role})"




# Faculty Assignment
class FacultyAssignment(models.Model):
    teacher = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'Teacher'}
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.user.username} → {self.subject.name}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        from .models import UserProfile
        UserProfile.objects.create(user=instance, role='Student')

