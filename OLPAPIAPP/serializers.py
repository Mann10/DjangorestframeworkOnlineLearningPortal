from rest_framework import serializers
from .models import *


class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseModel
        fields='__all__'
    
class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseModel
        exclude=('instructor',)
        