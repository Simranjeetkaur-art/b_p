from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.http import JsonResponse

from .serializers import UserSerializer

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        login(request, user)
        return Response({'user_id': user.id, 'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])
def google_login(request):
    try:
        # Perform the Google OAuth2 login here. You can use a library like python-social-auth to handle this.

        # If successful, create or retrieve the user
        user = User.objects.get_or_create(username='username', defaults={'email': 'example@example.com'})[0]

        # Log in the user
        login(request, user)

        # Generate a new access token
        refresh = RefreshToken.for_user(user)

        return Response({'user_id': user.id, 'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
    except OAuth2Error as e:
        return Response({'message': 'Google SSO login failed'}, status=status.HTTP_400_BAD_REQUEST)
