from rest_framework import serializers
from .models import User, Course, Cart

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
    class Meta:
        model = Cart
        fields = ['course', 'updated_at']