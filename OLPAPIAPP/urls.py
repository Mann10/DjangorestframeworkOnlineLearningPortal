from django.urls import path,include
from .views import *

urlpatterns = [
    path('courses/',CourseCreateView.as_view(),name='courses'),
    path('courses/<int:course_id>/',CourseDetailView.as_view(),name='course-id'),
    path('courses/create/',CourseCreateView.as_view(),name='courses-create'),
    path('courses/<int:course_id>/update/',CourseDetailView.as_view(),name='course-update'),
    path('courses/<int:course_id>/delete/',CourseDetailView.as_view(),name='course-update'),
    
]
