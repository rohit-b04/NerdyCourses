from rest_framework import serializers
from .models import User, Course, Cart, Section, Lecture

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name', 'email', 'role'
        ]
    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_title', 'course_description', 'price']

class CartSerializer(serializers.ModelSerializer):
    
    course = CourseSerializer()
    class Meta:
        model = Cart
        fields = ['course', 'updated_at']
        
class SectionSerializer(serializers.ModelSerializer):
    
    course = CourseSerializer()
    class Meta:
        model = Section
        fields = ['section_title', 'course']
        
class LectureSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    class Meta:
        model = Lecture
        fields = ['lecture_url', 'lecture_idx', 'section']