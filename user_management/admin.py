from django.contrib import admin
from .models import Student, Staff

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_first_name', 'get_last_name', 'program', 'semester', 'phone', 'get_email')
    search_fields = ('user__first_name', 'user__last_name', 'program__name', 'user__email')
    list_filter = ('program', 'semester')
    fields = (
        'user', 'program', 'semester', 'admission_number', 'roll_number', 'admission_year',
        'dob', 'blood_group', 'phone', 'address', 'pin_code',
        'father_name', 'mother_name', 'guardian_name', 'guardian_number', 'guardian_email',
        'tenth_percentage', 'twelfth_percentage', 'bachelor_percentage',
        'photo', 'identification_document'
    )

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "staff_id", "designation", "department")
    list_filter = ("designation", "department")
    search_fields = ("user__username", "staff_id", "designation", "department__name")

