from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_role_display', 'program', 'is_hod')
    list_filter = ('role', 'program', 'is_hod')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def get_role_display(self, obj):
        return obj.get_role_display()  # Displays the readable label instead of code
    get_role_display.short_description = 'Role'

