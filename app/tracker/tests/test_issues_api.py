"""
Test the issues API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Issue, Team

from tracker.serializers import IssueSerializer

ISSUES_URL = reverse("tracker:issue-list")


def detail_url(issue_id):
    """Return issue detail URL."""
    return reverse("issue:issue-detail", args=[issue_id])


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a sample user."""
    return get_user_model().objects.create_user(email=email, password=password)


def create_issue(user, **params):
    """Create and return a sample issue."""
    defaults = {
        "title": "Sample Issue",
        "description": "Sample Description",
        "status": "Open",
    }
    defaults.update(params)

    issue = Issue.objects.create(created_by=user, team=user.team, **defaults)

    return issue


class PublicIssueAPITests(TestCase):
    """Test the publically available issue API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving issues."""
        res = self.client.get(ISSUES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIssueAPITests(TestCase):
    """Test the private issue API."""

    def setUp(self):
        self.client = APIClient()
        team = Team.objects.create(name="Sample Team")
        self.user = create_user()
        self.user.team = team
        self.client.force_authenticate(self.user)

    def test_retrieve_issues(self):
        """Test retrieving issues in the API."""
        create_issue(user=self.user)
        create_issue(user=self.user)

        res = self.client.get(ISSUES_URL)

        issues = Issue.objects.all().order_by("-id")
        serializer = IssueSerializer(issues, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_issues_limited_to_members(self):
        """Test retrieving issues for user."""
        other_user = create_user(
            email="otheruser@example.com", password="testpassword123"
        )

        create_issue(user=other_user)

        create_issue(user=self.user)

        res = self.client.get(ISSUES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
