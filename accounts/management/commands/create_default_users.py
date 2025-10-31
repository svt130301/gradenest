from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from program_management.models import Program


class Command(BaseCommand):
    help = "Create default users (Admin, HOD, Teacher, Office Staff, Student)"

    def handle(self, *args, **options):
        users_data = [
            {"username": "admin", "password": "admin123", "role": "Admin"},
            {"username": "hod", "password": "hod123", "role": "Teacher"},
            {"username": "teacher", "password": "teacher123", "role": "Teacher"},
            {"username": "office", "password": "office123", "role": "OfficeStaff"},
            {"username": "student", "password": "student123", "role": "Student"},
        ]

        # Create a sample Program (if not already existing)
        program, _ = Program.objects.get_or_create(name="BCA", code="BCA01", duration=3)

        for data in users_data:
            user, created = User.objects.get_or_create(username=data["username"])
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {data['username']}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {data['username']} already exists."))

            # Attach or update profile
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = data["role"]
            if data["role"] in ["Teacher", "Student"]:
                profile.program = program
            profile.is_hod = (data["username"] == "hod")
            profile.save()

        self.stdout.write(self.style.SUCCESS("✅ Default users and program created successfully!"))

