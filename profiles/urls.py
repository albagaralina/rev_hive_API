from django.urls import path, include
from .views import register_user, login_user, email_confirmation, ProfileViewSet, UserViewSet, questionnaire, edit_profile, logout_user
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'users', UserViewSet)  # Add the UserViewSet here

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('confirm-email/<str:uidb64>/<str:token>/', email_confirmation),
    path('questionnaire/', questionnaire),
    path('edit-profile/', edit_profile),
    path('logout/', logout_user),
    path('', include(router.urls)),
]
