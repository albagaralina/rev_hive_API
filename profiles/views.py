# views.py
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
# ADDITIONS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
#ADDITIONS
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
#ADDITIONS
# views.py (additions)
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


@api_view(['POST'])
def register_user(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        Profile.objects.create(user=user)  # Automatically create a Profile for the new user
        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
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
