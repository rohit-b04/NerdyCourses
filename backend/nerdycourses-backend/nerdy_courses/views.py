from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import APIView
from datetime import datetime

from rest_framework_simplejwt.views import TokenObtainPairView

from nerdy_courses.models import *
# class User(APIView):
#     def register(self, request):
        


@api_view(['POST'])
@parser_classes([JSONParser])
def register(request):
    content = {"success": "User added successfully"}

    data = request.data
    # uid = data['uid']
    name = data['name']
    email = data['email']
    
    # cur.execute("select * from user where email = %s", (email,))
    email_exists = User.objects.all().filter(email=email)
    print(email_exists)
    if(len(email_exists) != 0):
        return Response({"message": "Email already exists"})
    password = data['password']
    created_at = datetime.now()
    u = User(name=name, email=email, password=password, created_at=created_at)
    u.save()
    # insert_query = "insert into user(uid, name, email, password, created_at) values(%s, %s, %s, %s, %s)"
    # insert_data = (uid, name, email, password, created_at)
    # cur.execute(insert_query, insert_data)
        

    return Response({"success": "User added successfully"}, status = status.HTTP_200_OK)

@api_view(['POST'])
@parser_classes([JSONParser])
def login(request):

    email = request.data['email']
    password = request.data['password']
            
    # fetch_data = "select email, password from user where email = %s and password = %s"
    # db_data = cur.execute(fetch_data, (email, password))
    fetch_data = User.objects.all().filter(email=email, password=password).values()
    # print(fetch_data)
    if(len(fetch_data) == 0):
        return Response({"status": "Login Failed"}, status = status.HTTP_202_ACCEPTED)

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

    result_courses = Course.objects.all().filter(id=course_id).values()
    # print(result_courses)
    if(len(result_courses) == 0):
        return Response({"message": "Cannot find the corresponding course"})
    return Response({"message": "success"})