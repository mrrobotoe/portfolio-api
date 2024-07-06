"""
Serializers for the tracker API
"""

from rest_framework import serializers

import datetime

from django.contrib.auth import get_user_model, authenticate

from django.contrib.auth import get_user_model, authenticate

from core.models import Issue, Organization, Project


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for issue objects."""

    # project = serializers.ForeignRelatedKey(Project, related_name="Project")
    project_name = serializers.ReadOnlyField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "status",
            "project",
            "project_name",
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
            "organization",
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
            "members",
            "created_at",
            "updated_at",
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for organization objects."""

    projects = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "projects",
            "members",
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        """Update Organization."""

        new_member = validated_data.pop("members", None)[0]

        instance.members.add(new_member)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class OrganizationDetailSerializer(OrganizationSerializer):
    """Serializer for organization detail view."""

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + [
            "projects",
            "members",
            "created_at",
            "updated_at",
        ]
