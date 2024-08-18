from django.shortcuts import render,get_object_or_404
from .models import *
from .views import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class CourseCreateView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        courses=CourseModel.objects.all().order_by('-created_at')
        ser=CourseModelSerializer(courses,many=True)
        return Response(ser.data)
    def post(self,request):
        ser=CourseModelSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data['title'])
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
class CourseDetailView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request,course_id):
        course=get_object_or_404(CourseModel,id=course_id)
        ser=CourseModelSerializer(course)
        return Response(ser.data)
        
        
    
    def put(self,request,course_id):
        course=get_object_or_404(CourseModel,id=course_id)
        ser=CourseUpdateSerializer(instance=course,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
        
        
    def delete(self,request,course_id):
        course=get_object_or_404(CourseModel,id=course_id)
        course.delete()
        return Response({'message':'Item Deleted Successfully!'})
