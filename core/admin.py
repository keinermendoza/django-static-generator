# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserAction

from django.utils.translation import gettext_lazy as _

class CustomUserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "usable_password", "password1", "password2"),
            },
        ),
    )

@admin.register(CustomUser)
class CustomUserAdmin(CustomUserModelAdmin):
    list_display = ["email", "name","is_admin", "is_active"]
    list_display_links = ["email"]
    filter_horizontal = []
    list_filter = []
    fieldsets = []
    ordering = ["email"]

    
@admin.register(UserAction)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["user"]

