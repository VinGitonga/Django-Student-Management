from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('dept/create/', DepartmentCreateView.as_view(), name='dept-create'),
    path('dept/update/<int:pk>/', DepartmentUpdateView.as_view(), name='dept-update'),
    path('dept/delete/<int:pk>/', DepartmentDeleteView.as_view(), name='dept-delete'),
    path('dept/list/', DepartmentListView.as_view(), name='dept-list'),
    path('course/create/', CourseCreateView.as_view(), name='course-create'),
    path('course/update/<int:pk>/', CourseUpdateView.as_view(), name='course-update'),
    path('course/list/', CourseListView.as_view(), name='course-list'),
    path('course/delete/<int:pk>/', CourseDeleteView.as_view(), name='course-delete'),
    path('student/create/', StudentCreateView.as_view(), name='student-create'),
    path('student/list/', StudentListView.as_view(), name='student-list'),
    path('student/details/<int:pk>/', StudentDetailView.as_view(), name='student-details'),
    path('student/update/<int:pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('student/delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),

]