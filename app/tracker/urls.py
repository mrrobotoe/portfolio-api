"""
URL mappings for the tracker API.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from tracker import views

router = DefaultRouter()
router.register("issues", views.IssueViewSet)
router.register("projects", views.ProjectViewSet)
router.register("teams", views.TeamViewSet)

app_name = "tracker"

urlpatterns = [
    path("", include(router.urls)),
]
