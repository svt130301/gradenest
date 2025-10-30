
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.CharField(max_length=50, help_text="e.g., 2 Years, 3 Years")
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='subjects')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    semester = models.IntegerField()
    has_lab = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.program.name})"
