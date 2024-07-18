"""
Test the project API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Team, Project

from tracker.serializers import ProjectSerializer

PROJECTS_URL = reverse("tracker:project-list")


def detail_url(project_id):
    """Return project detail URL."""
    return reverse("tracker:project-detail", args=[project_id])


def create_team(user, **params):
    """Create and return a sample organization."""
    defaults = {
        "name": "Sample Organization",
    }

    defaults.update(params)

    team = Team.objects.create(**defaults)
    team.members.add(user)
    team.save()
    return team


def create_project(user, team, **params):
    """Create and return a sample project."""
    defaults = {
        "name": "Sample Project",
    }
    defaults.update(params)

    project = Project.objects.create(team=team, **defaults)
    project.members.add(user)
    project.save()
    return project


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a sample user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicProjectAPITests(TestCase):
    """Test the publically available project API."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving projects."""
        res = self.client.get(PROJECTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivaeProjectAPITests(TestCase):
    """Test the private project API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_projects(self):
        """Test retrieving projects."""
        team = create_team(user=self.user)
        create_project(user=self.user, team=team)
        create_project(user=self.user, team=team)

        res = self.client.get(PROJECTS_URL)

        projects = Project.objects.all().order_by("-name")
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_retrieve_projects_limited_to_members(self):
    #     """Test retrieving projects for members."""
    #     team = create_team(user=self.user)
    #     create_project(user=self.user, team=team)
    #     other_user = create_user(
    #         email="testuser@example.com", password="testpass123"
    #     )
    #     create_project(user=other_user, team=team)

    #     res = self.client.get(PROJECTS_URL)

    #     projects = Project.objects.filter(members=self.user)
    #     serializer = ProjectSerializer(projects, many=True)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 2)
    #     self.assertEqual(res.data, serializer.data)
