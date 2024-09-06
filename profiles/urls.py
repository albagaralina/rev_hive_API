from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import ProfileViewSet, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token

# Set up the DRF router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),  # DRF API routes for users and profiles
    path('token-auth/', obtain_auth_token),  # Token authentication endpoint
]
