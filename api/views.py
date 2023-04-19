from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Pet


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
            userData = User.objects.get(id=token.user.id)

            response_data = {
                'token': token.key,
                'data': {
                    'first_name': userData.first_name,
                    'last_name': userData.last_name,
                    'email': userData.email,
                    'id': userData.id
                }
            }
            return Response(response_data)
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


class Profile(APIView):
    def post(self, request):
        getToken = request.data.get('headers').get('Authorization')
        token = Token.objects.get(key=getToken)
        user_id = token.user.id
        with connection.cursor() as cursor:
            cursor.execute('SELECT username,'
                           'first_name,'
                           'last_name,'
                           'email,'
                           'phone,'
                           'city,'
                           'state,'
                           'zipcode'
                           ' FROM auth_user where id = %s', [user_id])
            data = cursor.fetchall()

        return JsonResponse({'message': data})


#@method_decorator(permission_required('view_pet'), name='dispatch')
class Mypet(APIView):
    def post(self, request):
        #getToken = request.data.get('headers').get('Authorization')
        user = User.objects.get(username='mike1')
        task = Pet.objects.get(pk=1)
        #assign_perm('view_pet', user, task)
        # token = Token.objects.get(key='83ac0d1c3d89ba566db9a1d371ac0d5e2db24d72')
        # user_id = token.user.id
        # with connection.cursor() as cursor:
        #     cursor.execute('SELECT * FROM api_pet where id = 1')
        #     data = cursor.fetchall()
        has_view_permission = user.has_perm('view_pet', task)
        if has_view_permission:
            msg = 'Alice has the view_task permission for the task'
        else:
            msg = 'Alice does not have the view_task permission for the task'
        return JsonResponse({'message': msg})
