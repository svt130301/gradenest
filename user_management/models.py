from django.db import models
from django.contrib.auth.models import User
from program_management.models import Program, Department

# ----------------- Student -----------------
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.PositiveIntegerField(default=1)
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    admission_year = models.PositiveIntegerField(null=True, blank=True)

    # Personal info
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pin_code = models.CharField(max_length=10, blank=True, null=True)

    # Family details
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_number = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)

    # Academic info
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bachelor_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Documents
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    identification_document = models.FileField(upload_to='students/id_docs/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.program.name if self.program else 'No Program'})"


# ----------------- Staff -----------------
class Staff(models.Model):
    DESIGNATION_CHOICES = [
        ("Assistant Professor", "Assistant Professor"),
        ("Associate Professor", "Associate Professor"),
        ("Professor", "Professor"),
        ("Office staff", "Office staff"),
        ("Other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    staff_id = models.CharField(max_length=20, unique=True)

    designation = models.CharField(max_length=100, choices=DESIGNATION_CHOICES, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    # Personal info
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        blank=True, null=True
    )
    blood_type = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('O+', 'O+'), ('O-', 'O-'),
            ('AB+', 'AB+'), ('AB-', 'AB-')
        ],
        blank=True, null=True
    )

    # Documents
    identification_document = models.FileField(upload_to='staff/id_docs/', blank=True, null=True)
    photo = models.ImageField(upload_to='staff/photos/', blank=True, null=True)

    # Education
    educational_qualification = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.userprofile.role})"

