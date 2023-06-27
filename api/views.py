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
import bcrypt
import json
import sys
import os
 
from datetime import datetime, date

@api_view(['POST'])
def hello_world(request):
    return JsonResponse({'message': 'Hello, world!'})
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        with connection.cursor() as cursor:
            cursor.execute(f"select * from auth_user where email = '{email}'")
            check = cursor.fetchone()
            if check is not None:
                user = authenticate(username=email, password=password)

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
            else:
                cursor.execute(f"select * from users where email = '{email}'")
                row = cursor.fetchone()
                if row:
                    hashCode = row[5]
                    if bcrypt.checkpw(password.encode('utf-8'), hashCode.encode('utf-8')):
                        identify = 1
                    else:
                        identify = 0
                else:
                    return Response('user not found at existing Database')
                if identify == 1:
                    try:

                             branch_id = row[1]
                             first_name = row[2]
                             last_name = row[3]
                             email = row[4]
                             company_id = row[9]
                             extn_email1 = row[10]
                             extn_email2 = row[11]
                             extn_email3 = row[12]
                            # Create new user
                             user = User.objects.create_user(username=email,
                                                            email=email,
                                                            password=password,
                                                            first_name=first_name,
                                                            last_name=last_name,
                                                            )
                             user_id = user.id
                             updateuserData = connection.cursor()
                             query = "UPDATE auth_user SET branch_id=%s,company_id=%s, extn_email1=%s, extn_email2=%s, extn_email3=%s, oldid=%s WHERE id=%s"
                             params = (branch_id, company_id, extn_email1, extn_email2, extn_email3, row[0], user_id)

                             updateuserData.execute(query,params)
                             connection.commit()
                             return Response({'message': 'User created successfully'})
                    except IntegrityError as e:
                                 return Response(e)



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
        #getToken = request.data.get('headers').get('Authorization')
        token = Token.objects.get(key='d579b045a4f38e7cf534354fe10b763f7700764a')
        user_id = token.user.id
        with connection.cursor() as cursor:

            #user
            cursor.execute(f"select id,username,first_name,last_name,branch_id,company_id,oldid from auth_user where id= {user_id}")
            columns = [col[0] for col in cursor.description]
            rows = []
            for row in cursor.fetchall():
                rows.append(dict(zip(columns, row)))
            json_data = json.dumps(rows, cls=DateTimeEncoder)
            userData = json.loads(json_data)

            #branch
            cursor.execute(f"select * from branches where id= {userData[0]['branch_id']}")
            columns = [col[0] for col in cursor.description]
            rows = []
            for row in cursor.fetchall():
                rows.append(dict(zip(columns, row)))
            json_data = json.dumps(rows, cls=DateTimeEncoder)
            branchData = json.loads(json_data)

            #company
            cursor.execute(f"select * from companies where id= {userData[0]['company_id']}")
            columns = [col[0] for col in cursor.description]
            rows = []
            for row in cursor.fetchall():
                rows.append(dict(zip(columns, row)))
            json_data = json.dumps(rows, cls=DateTimeEncoder)
            companyData = json.loads(json_data)

            #employment
            cursor.execute(f"select * from user_employments where id= {userData[0]['oldid']}")
            columns = [col[0] for col in cursor.description]
            rows = []
            for row in cursor.fetchall():
                rows.append(dict(zip(columns, row)))
            json_data = json.dumps(rows, cls=DateTimeEncoder)
            employmentData = json.loads(json_data)

            division_id = employmentData[0]['division_id']
            department_id = employmentData[0]['department_id']

            if division_id is None:
                division_id = 4
            if department_id is None:
                department_id = 18


            #division
            cursor.execute(f"select * from divisions where id= { division_id }")
            columns = [col[0] for col in cursor.description]
            rows = []
            for row in cursor.fetchall():
                rows.append(dict(zip(columns, row)))
            json_data = json.dumps(rows, cls=DateTimeEncoder)
            divisionData = json.loads(json_data)


            #department
            cursor.execute(f"select * from departments where id= { department_id }")
            columns = [col[0] for col in cursor.description]
            rows = []
            for row in cursor.fetchall():
                rows.append(dict(zip(columns, row)))
            json_data = json.dumps(rows, cls=DateTimeEncoder)
            departmentData = json.loads(json_data)

            #QueryAll
            userData[0]['branch'] = branchData[0]
            userData[0]['company'] = companyData[0]
            userData[0]['employment'] = employmentData[0]
            userData[0]['division'] = divisionData[0]
            userData[0]['department'] = departmentData[0]

            return Response(userData, content_type="application/json")

#@method_decorator(permission_required('view_pet'), name='dispatch')
# class Mypet(APIView):
#     def post(self, request):
#         #getToken = request.data.get('headers').get('Authorization')
#         user = User.objects.get(username='mike1')
#         task = Pet.objects.get(pk=1)
#         #assign_perm('view_pet', user, task)
#         # token = Token.objects.get(key='83ac0d1c3d89ba566db9a1d371ac0d5e2db24d72')
#         # user_id = token.user.id
#         # with connection.cursor() as cursor:
#         #     cursor.execute('SELECT * FROM api_pet where id = 1')
#         #     data = cursor.fetchall()
#         has_view_permission = user.has_perm('view_pet', task)
#         if has_view_permission:
#             msg = 'Alice has the view_task permission for the task'
#         else:
#             msg = 'Alice does not have the view_task permission for the task'
#         return JsonResponse({'message': msg})
class MyBranch(APIView):
    def get(self, request):
        page = request.GET.get('page', 1)
        per_page = request.GET.get('perPage', 10)
        search_query = request.GET.get('search')  # get the search query parameter
        with connection.cursor() as cursor:
            start_index = (int(page) - 1) * int(per_page)
            cursor.execute(f"SELECT COUNT(*) FROM branches WHERE name LIKE '%{search_query}%'")
            total_rows = cursor.fetchone()[0]
            cursor.execute(
                f"SELECT * FROM branches WHERE name LIKE '%{search_query}%' LIMIT {per_page} OFFSET {start_index}")
            data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return JsonResponse({'rows': data, 'totalRows': total_rows})

class testSAP(APIView):
    def post(self, request):

        return JsonResponse({"message": ''})

