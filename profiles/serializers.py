from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'profileID', 'user_name', 'company_name', 'job_title', 'years_of_experience', 'bio', 'phone', 'image', 'email', 'has_completed_questionnaire']

