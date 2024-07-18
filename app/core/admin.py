"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
        (_("Team"), {"fields": ("team",)}),
    )

    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


class UserInline(admin.TabularInline):
    model = models.User
    fields = ("email", "projects")
    readonly_fields = ("email",)
    extra = 0


class TeamAdmin(admin.ModelAdmin):
    """Define admin pages for teams."""

    model = models.Team
    inlines = [
        UserInline,
    ]
    ordering = ["id"]

    list_display = [
        "name",
    ]
    fieldsets = ((None, {"fields": ("name",)}),)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Project)
admin.site.register(models.Issue)
admin.site.register(models.Team, TeamAdmin)
