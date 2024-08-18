from rest_framework import serializers
from .models import *



    
class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseModel
        exclude=('instructor',)
        
class EnrollmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=EnrollmentModel
        fields='__all__'
    
        
class LessonModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=LessonModel
        fields='__all__'
        
class CourseModelSerializer(serializers.ModelSerializer):
    lesson_course=LessonModelSerializer(many=True,read_only=True)
    
    class Meta:
        model=CourseModel
        fields='__all__'
        

    