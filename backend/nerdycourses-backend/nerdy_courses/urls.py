from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register),
    # path("api/login", views.login),
    path("logout", views.logout),
    path("search-courses", views.search_courses),
    path("course", views.course),
    path("cart", views.cart),
    path("instructor", views.instructor)
]