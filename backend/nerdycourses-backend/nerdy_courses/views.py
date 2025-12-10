from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from nerdy_courses.models import *
from .serializers import CourseSerializer, UserSerializer, CartSerializer, SectionSerializer

@api_view(['POST'])
@parser_classes([JSONParser])
def register(request):
    data = request.data
    name = data['name']
    email = data['email']
    
    email_exists = User.objects.filter(email=email).exists()
    if(email_exists != False):
        return Response({"message": "Email already exists"})
    
    password = data['password']
    u = User.objects.create_user(email=email, name=name, password=password)
    
    serializer = UserSerializer(u)
    return Response({"success": "User added successfully", "data": serializer.data}, status = status.HTTP_200_OK)

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

    result_courses = Course.objects.filter(id=course_id)
    serializer = CourseSerializer(result_courses, many=True)
    
    # print(result_courses)
    if(len(result_courses) == 0):
        return Response({"message": "Cannot find the corresponding course"})
    return Response({"data": serializer.data})

@api_view(['GET'])
def courses(request):
    course_instance = Course.objects.all()
    course_serializer = CourseSerializer(course_instance, many=True)
    return Response(course_serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def course(request):
    if request.user.role != 'instructor':
        return Response({"message": "Only Instructor can add course"})
    instructorId = Instructor.objects.get(user=request.user)
    # print(type(instructorId))
    findcourse = Course.objects.filter(course_title=request.data['title'], instructor_id=instructorId).exists()
    if findcourse == True:
        raise NameError('Course title already exists')
    instance = Course.objects.create(
                    course_title=request.data['title'], 
                    course_description=request.data['description'], 
                    instructor_id=instructorId.pk, 
                    price=request.data['price']
                )
    instance.save()
    return Response({"message": "Course added successfully"}, status=200)
    
    
@api_view(['POST']) 
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def cart(request):
    data = request.data
    u = request.user
    
    userInstance = User.objects.get(name=data['instructor'])
    instructor = Instructor.objects.get(user=userInstance).pk
    course=Course.objects.get(course_title=data['title'], instructor=instructor)
    
    cart_instance = Cart.objects.filter(user=u, course=course)
    if(cart_instance.exists() == True):
        return Response({"message": "Cart item already added"})
    
    cartData = Cart.objects.create(user=u, course=course)
    cartData.save()
    return Response({"message": "Item added to cart successfully"}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_cart(request):
    user = request.user
    
    cart_instance = Cart.objects.filter(user=user)
    serializer = CartSerializer(cart_instance, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def section(request):
    if request.user.role != 'instructor':
        return Response({"message": "Only Instructor can add section to course"})
    section_title = request.data['section_title']
    course = Course.objects.get(course_title=request.data['course_title'])
    if(Section.objects.filter(section_title=section_title, course=course.pk).exists() == True):
        return Response({"Message": "Similar section already exists in the course"})
    section_data = Section.objects.create(section_title=section_title, course=course)
    
    return Response({"message": "Section added to course"})

@api_view(['GET'])
def section_get(request):
    section = request.GET.get('section-id')
    course = request.GET.get('course-id')
    data = Section.objects.filter(id=section, course=course)
    serializer = SectionSerializer(data, many=True)
    
    return Response(serializer.data)