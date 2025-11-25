from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from rest_framework_simplejwt.views import TokenObtainPairView
from .managers import CustomUserManager

class OrderStatus(models.TextChoices):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    
class PaymentStatus(models.TextChoices):
    INITIATED = "initiated"
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class User(AbstractBaseUser):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name']
    objects = CustomUserManager()
        

class Instructor(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=255, null=False)
    instructor_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Course(models.Model):
    course_title = models.CharField(null=False, max_length=255)
    course_description = models.TextField()
    price = models.FloatField(null=False, default=0.0)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Section(models.Model):
    section_title = models.CharField(max_length=255, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Lecture(models.Model):
    lecture_title = models.CharField(null=False, max_length=255)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    lecture_url = models.CharField(max_length=255)
    lecture_idx = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Progress(models.Model):
    watched_seconds = models.FloatField(null=False, default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

class Order(models.Model):
    amount = models.FloatField(null=False, default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length = 15, choices=OrderStatus.choices)
    attempts = models.IntegerField(default=1)
    
class Payment(models.Model):
    provider_txn = models.CharField(max_length=255, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=15, choices=PaymentStatus.choices)
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    