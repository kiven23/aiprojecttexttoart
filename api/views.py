from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.db import IntegrityError


@api_view(['POST'])
def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})
class UserLoginAPIView(APIView):
    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateUser(APIView):
    def post(self, request):
        try:
            # Get user data from request
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            # Create new user
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=first_name,
                                            last_name=last_name)

            # Return success message
            return Response({'message': 'User created successfully'})
        except IntegrityError as e:
            # Raise validation error
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

