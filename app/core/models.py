"""
Database models.
"""

from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save and return superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def __str__(self):
        return self.email


class Team(models.Model):
    """Team objects."""

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    """Project objects."""

    team = models.ForeignKey(
        Team, related_name="projects", on_delete=models.DO_NOTHING
    )

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def team_name(self):
        return self.team.name


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    USER_ROLES = [
        (1, "ADMIN"),
        (2, "USER"),
    ]

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    user_role = models.CharField(
        max_length=150, default="2", choices=USER_ROLES
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    team = models.ForeignKey(
        Team,
        related_name="members",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    projects = models.ForeignKey(
        Project,
        related_name="members",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def team_name(self):
        return self.team.name


class Issue(models.Model):
    """Issue objects."""

    project = models.ForeignKey(
        Project,
        related_name="issues",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    team = models.ForeignKey(
        Team, related_name="issues", on_delete=models.DO_NOTHING, null=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=150, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_by_user",
        on_delete=models.DO_NOTHING,
        null=True,
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="assigned_to_user",
        on_delete=models.DO_NOTHING,
        null=True,
    )

    def __str__(self):
        return self.title

    @property
    def project_name(self):
        return self.project.name

    @property
    def team_name(self):
        return self.team.name


class Comment(models.Model):
    """Comment objects."""

    issue = models.ForeignKey(
        Issue,
        related_name="comments",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="commented_by_user",
        on_delete=models.DO_NOTHING,
        null=True,
    )

    def __str__(self):
        return self.comment
