from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status


from nerdy_courses.models import *
from nerdy_courses.managers import CustomUserManager


@api_view(['POST'])
@parser_classes([JSONParser])
def register(request):
    data = request.data
    name = data['name']
    email = data['email']
    
    email_exists = User.objects.all().filter(email=email)
    print(email_exists)
    if(len(email_exists) != 0):
        return Response({"message": "Email already exists"})
    password = data['password']
    u = User.objects.create_user(email=email, name=name, password=password)
    return Response({"success": "User added successfully", "data": f'{u}'}, status = status.HTTP_200_OK)

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

