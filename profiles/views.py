# views.py

from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rev_hive_API.settings import EMAIL_FROM
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def register_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user.is_active = False  # Mark the user as inactive until email confirmation
        user.save()

        # Create associated Profile
        Profile.objects.create(user=user)

        # Send email confirmation
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirmation_link = request.build_absolute_uri(f'/api/confirm-email/{uidb64}/{token}/')

        email_subject = 'Confirm Your Registration'
        email_message = f'Please confirm your registration by clicking the following link: {confirmation_link}'
        
        send_mail(email_subject, email_message, EMAIL_FROM, [user.email])

        return Response({'message': 'User registered successfully! Check your email for confirmation.'}, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def email_confirmation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Email confirmed successfully!'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid confirmation link.'}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


@api_view(['POST'])
def questionnaire(request):
    if request.method == "POST":
        employment_status = request.data.get('employment_status')
        job_title = request.data.get('job_title')
        industry = request.data.get('industry')
        reason_for_joining = request.data.get('reason_for_joining')

        # Create a plain text email message with the user's responses
        email_subject = f'Questionnaire Submission for {request.user.username}'
        email_message = (
            f'1. Are you currently: {employment_status}\n'
            f'2. Which job title most accurately identifies you?: {job_title}\n'
            f'3. What industry do you work in?: {industry}\n'
            f'4. What brought you to Revenue Hive?: {reason_for_joining}'
        )

        # Send the email
        send_mail(email_subject, email_message, EMAIL_FROM, ['matt@revenuehive.io'])

        # Mark the user profile as having completed the questionnaire
        profile = Profile.objects.get(user=request.user)
        profile.has_completed_questionnaire = True
        profile.save()

        return Response({'message': 'Questionnaire submitted successfully!'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_user(request):
    request.auth.delete()  # Delete the token to log out
    return Response({'message': 'Logged out successfully!'}, status=status.HTTP_200_OK)
