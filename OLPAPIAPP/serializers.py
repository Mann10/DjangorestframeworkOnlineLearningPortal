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
    enrolled_course=EnrollmentModelSerializer(many=True,read_only=True)
    
    class Meta:
        model=CourseModel
        fields='__all__'
        
class ProgressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProgressModel
        fields='__all__'
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model=AnswerModel
        fields='__all__' 
        

class QuestionSerializer(serializers.ModelSerializer):
    question=AnswerSerializer(read_only=True,many=True)
    class Meta:
        model=QuestionModel
        fields='__all__'       
        
class CreateQuizModelSerializer(serializers.ModelSerializer):
    questions= QuestionSerializer(read_only=True,many=True)
    question=AnswerSerializer(read_only=True,many=True)
    class Meta:
        model=QuizModel
        fields='__all__'
    
class ResultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResultModel
        fields='__all__'