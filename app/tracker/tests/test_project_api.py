"""
Test the project API.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Organization, Project

from tracker.serializers import ProjectSerializer

PROJECTS_URL = reverse("tracker:project-list")


def detail_url(project_id):
    """Return project detail URL."""
    return reverse("tracker:project-detail", args=[project_id])


def create_organization(user, **params):
    """Create and return a sample organization."""
    defaults = {
        "name": "Sample Organization",
    }

    defaults.update(params)

    organization = Organization.objects.create(**defaults)
    organization.members.add(user)
    organization.save()
    return organization


def create_project(user, organization, **params):
    """Create and return a sample project."""
    defaults = {
        "name": "Sample Project",
    }
    defaults.update(params)

    project = Project.objects.create(organization=organization, **defaults)
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
        organization = create_organization(user=self.user)
        create_project(user=self.user, organization=organization)
        create_project(user=self.user, organization=organization)

        res = self.client.get(PROJECTS_URL)

        projects = Project.objects.all().order_by("-name")
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_projects_limited_to_members(self):
        """Test retrieving projects for members."""
        organization = create_organization(user=self.user)
        create_project(user=self.user, organization=organization)
        other_user = create_user(
            email="testuser@example.com", password="testpass123"
        )
        create_project(user=other_user, organization=organization)

        res = self.client.get(PROJECTS_URL)

        projects = Project.objects.filter(members=self.user)
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
