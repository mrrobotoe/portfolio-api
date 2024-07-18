"""
Test for custom models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a value error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testpass123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com", "testpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_team(self):
        """Test creating a Team."""
        team = models.Team.objects.create(
            name="Test Team",
        )

        self.assertEqual(str(team), team.name)

    def test_create_project(self):
        """Test creating a project."""
        team = models.Team.objects.create(
            name="Test Team",
        )

        project = models.Project.objects.create(
            team=team,
            name="Test Project",
        )

        self.assertEqual(str(project), project.name)

    def test_create_issue(self):
        """Test creating an issue."""
        team = models.Team.objects.create(
            name="Test Team",
        )

        project = models.Project.objects.create(
            name="Test Project",
            team=team,
        )

        issue = models.Issue.objects.create(
            project=project,
            title="Test Issue",
            description="Test issue description",
            status="Open",
        )

        self.assertEqual(str(issue), issue.title)
