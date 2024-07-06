"""
Views for the user API.
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""

    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token."""

    serializer_class = AuthTokenSerializer
    renderer_classes = (
        api_settings.DEFAULT_RENDERER_CLASSES
    )  # we wouldn't get the browsable api for rest_framework UI


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, format=None):
        """Retrieve and return authenticated user."""
        # if self.request.auth is None or self.request.user.is_anonymous:
        #     return Response(
        #         {"detail": "Update message."},
        #         status=status.HTTP_200_OK,
        #     )

        return self.request.user
