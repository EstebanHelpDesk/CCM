from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Student, ResponsibleStudent, LateArrival

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("id_number", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "is_school_staff", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("id_number", "full_name", "email", "password1", "password2"),
        }),
    )
    list_display = ("id_number", "full_name", "email", "is_school_staff", "is_staff", "is_superuser")
    search_fields = ("id_number", "full_name", "email")
    ordering = ("id_number",)

admin.site.register(Student)
admin.site.register(ResponsibleStudent)
admin.site.register(LateArrival)
