from django.http import JsonResponse
from django.db import connections
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import APIView
from datetime import datetime

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *
# class User(APIView):
#     def register(self, request):
        


@api_view(['POST'])
@parser_classes([JSONParser])
def register(request):
    content = {"success": "User added successfully"}
    try:
        conn = connections.create_connection('default')
        with conn.cursor() as cur:
            data = request.data
            uid = data['uid']
            name = data['name']
            email = data['email']
            cur.execute("select * from user where email = %s", (email,))
            email_exists = cur.fetchall()
            if(len(email_exists) != 0):
                return Response({"account": "User already exists"})
            password = data['password']
            created_at = datetime.now()
            insert_query = "insert into user(uid, name, email, password, created_at) values(%s, %s, %s, %s, %s)"
            insert_data = (uid, name, email, password, created_at)
            cur.execute(insert_query, insert_data)
        
    except Exception as e:
        print(e)
        return Response({"Error": f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"success": "User added successfully"}, status = status.HTTP_200_OK)

@api_view(['POST'])
@parser_classes([JSONParser])
def login(request):
    
    try:
        conn = connections.create_connection('default')
        email = request.data['email']
        password = request.data['password']

        with conn.cursor() as cur:
            fetch_data = User.objects.get(email=email)
            fetch_data = "select email, password from user where email = %s and password = %s"
            db_data = cur.execute(fetch_data, (email, password))

            if(db_data == 0):
                return Response({"status": "Login Failed"}, status = status.HTTP_202_ACCEPTED)

    except Exception as e:
        return Response({"error": f"{e}"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"success": "Logged in successfully"}, status = status.HTTP_200_OK)

@api_view(['DELETE'])
@parser_classes([JSONParser])
def logout(request):
    #Ending the jwt session 
    return Response({"success": "Logged out successfully"})

@api_view(['GET'])
@parser_classes([JSONParser])
def search_courses(request):
    course_id = request.GET['course-id']
    try:
        conn = connections.create_connection('default')
        with conn.cursor() as cur:
            cur.execute("select * from course where course_id = %s", (course_id,))
            result_courses = cur.fetchone()
            print(result_courses)
    except Exception as e:
        return Response({"Error": f'{e}'})
    return Response({"data": "success"})