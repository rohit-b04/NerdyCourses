from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from nerdy_courses.models import *


@api_view(['POST'])
@parser_classes([JSONParser])
def register(request):
    data = request.data
    name = data['name']
    email = data['email']
    
    email_exists = User.objects.filter(email=email).exists()
    # print(email_exists)
    if(email_exists != False):
        return Response({"message": "Email already exists"})
    password = data['password']
    u = User.objects.create_user(email=email, name=name, password=password)
    return Response({"success": "User added successfully", "data": f'{u}'}, status = status.HTTP_200_OK)

@api_view(['DELETE'])
@parser_classes([JSONParser])
def logout(request):
    #Ending the jwt session 
    return Response({"success": "Logged out successfully"})


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def instructor(request):
    
    email_exists = User.objects.filter(email=request.data['email']).exists()
    if(email_exists == True):
        return Response({"message": "Email already exists"})
    instance = User.objects.create_user(
                    name=request.data['name'], 
                    email=request.data['email'], 
                    password=request.data['password'],
                    role='instructor'
                )
    instance.save()
    teacher = Instructor.objects.create(user=instance, description=request.data['description'])
    teacher.save()
    return Response({"message": "Instructor registered successfully"}, status=200)


@api_view(['GET'])
@parser_classes([JSONParser])
def search_courses(request):
    course_id = request.GET['course-id']

    result_courses = Course.objects.all().filter(id=course_id).values()
    # print(result_courses)
    if(len(result_courses) == 0):
        return Response({"message": "Cannot find the corresponding course"})
    return Response({"message": "success"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course(request):
    if not request.user.is_staff:
        return Response({"detail": "unauthorized"}, status=403)
    instance = Course.objects.create(course_title=request.data['title'], description=request.data['description'], instructor=request.data['instructor'], price=request.data['price'])
    instance.save()
    return Response({"message": "Course added successfully"}, status=200)
    
    
@api_view(['POST']) 
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def cart(request):
    u = request.user
    c = request.course
    cartData = Cart.objects.create(user=u, course=c)
    cartData.save()
    return Response({"message": "Item added to cart successfully"})