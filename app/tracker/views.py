"""
Views for the tracker APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Issue, Team, Project
from tracker import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """View for manage projects in tracker APIs."""

    serializer_class = serializers.ProjectDetailSerializer
    queryset = Project.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new project."""
        serializer.save(team=[self.request.user])

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == "list":
            return serializers.ProjectSerializer

        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(team__id=self.request.user.team.id)


class IssueViewSet(viewsets.ModelViewSet):
    """View for manage issues in tracker APIs."""

    serializer_class = serializers.IssueDetailSerializer
    queryset = Issue.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve issues for authenticated user."""
        if self.request.user.team is not None:
            return self.queryset.filter(
                team__id=self.request.user.team.id
            ).order_by("-id")

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == "list":
            return serializers.IssueSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new issue."""
        team = Team.objects.get(id=self.request.user.team.id)
        serializer.save(created_by=self.request.user)
        serializer.save(team=team)


class TeamViewSet(viewsets.ModelViewSet):
    """View for manage teams in tracker APIs."""

    serializer_class = serializers.TeamDetailSerializer
    queryset = Team.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == "list":
            return serializers.TeamSerializer

        return self.serializer_class

    def get_queryset(self):
        """Retrieve teams for authenticated user."""
        return self.queryset.filter(members=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        """Create a new teams."""
        serializer.save(members=[self.request.user])
