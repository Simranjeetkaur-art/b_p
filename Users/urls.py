from django.urls import path

from .views import UserListView, UserDetailsView, GoogleLogin

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailsView.as_view(), name='user-details'),
    path('google-login/', GoogleLogin.as_view(), name='google-login'),
]
