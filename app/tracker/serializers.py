"""
Serializers for the tracker API
"""

from rest_framework import serializers

import datetime

from core.models import Issue, Team, Project, User


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for issue objects."""

    team = serializers.StringRelatedField(
        read_only=True,
        required=False,
    )

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "status",
            "project",
            "team",
            "created_at",
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        """Update Issue."""
        instance.updated_at = datetime.datetime.now()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class IssueDetailSerializer(IssueSerializer):
    """Serializer for issue detail view."""

    class Meta(IssueSerializer.Meta):
        fields = IssueSerializer.Meta.fields + [
            "updated_at",
            "assigned_to",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "created_by"]


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for project objects."""

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "team",
        ]
        read_only_fields = ["id"]


class ProjectDetailSerializer(ProjectSerializer):
    """Serializer for project detail view."""

    issues = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        required=False,
    )

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + [
            "issues",
            "team",
            "created_at",
            "updated_at",
        ]


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for team objects."""

    projects = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        required=False,
    )

    members = serializers.StringRelatedField(
        many=True,
        read_only=True,
        required=False,
    )

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "projects",
            "members",
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        """Update Team."""
        if "members" in self.context["request"].data:
            for member in self.context["request"].data["members"]:
                instance.members.add(User.objects.get(id=member))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TeamDetailSerializer(TeamSerializer):
    """Serializer for team detail view."""

    class Meta(TeamSerializer.Meta):
        fields = TeamSerializer.Meta.fields + [
            "projects",
            "created_at",
            "updated_at",
        ]
