from django.shortcuts import render,get_object_or_404
from .models import *
from .views import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


from .custom_permission import *
# Create your views here.

class CourseCreateView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,(IsStudentAndReadOnlyCourses|IsIntructorCanCreateUpdateDestroyCourse|IsAdmin)]
    
    
    def get(self,request):
        courses=CourseModel.objects.all().order_by('-created_at')
        ser=CourseModelSerializer(courses,many=True)
        return Response(ser.data)
    def post(self,request):
        ser=CourseModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
class CourseDetailView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,(IsStudentAndReadOnlyCourses|IsIntructorCanCreateUpdateDestroyCourse|IsAdmin)]
    
    def get(self,request,course_id):
        course=get_object_or_404(CourseModel,id=course_id)
        ser=CourseModelSerializer(course)
        return Response(ser.data)
        
        
    
    def put(self,request,course_id):
        course=get_object_or_404(CourseModel,id=course_id)
        self.check_object_permissions(request,course)
        ser=CourseUpdateSerializer(instance=course,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
        
        
    def delete(self,request,course_id):
        course=get_object_or_404(CourseModel,id=course_id)
        self.check_object_permissions(request,course)
        course.delete()
        return Response({'message':'Item Deleted Successfully!'})


class EnrollmentCreateView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsStudentCanManageOwnEnrollement|IsAdmin]
    
    def get(self,request):
        enrollments=EnrollmentModel.objects.all()
        ser=EnrollmentModelSerializer(enrollments,many=True)
        return Response(ser.data)
    def post(self,request,course_id):
        course=get_object_or_404(CourseModel,id=course_id)
        data={'user':self.request.user.id,'course':course.pk}
        ser=EnrollmentModelSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
class EnrollmentDetailView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,IsStudentCanManageOwnEnrollement|IsAdmin]
    
    def get(self,request,enrollment_id):
        enl=get_object_or_404(EnrollmentModel,id=enrollment_id)
        self.check_object_permissions(request, enl)
        ser=EnrollmentModelSerializer(enl)
        return Response(ser.data)
    
    def delete(self,request,enrollment_id):
        enl=get_object_or_404(EnrollmentModel,id=enrollment_id)
        self.check_object_permissions(request, enl)
        enl.delete()
        return Response({'message':'Item Deleted Successfully!'})
    

class LessonDetailCrudView(APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,(IsStudentAndReadOnlyCourses|IsInstructorCreateupdatedeletelessons|IsAdmin)]
    
    def get(self,request,lesson_id):
    
        lesson=get_object_or_404(LessonModel,id=lesson_id)
        ser=LessonModelSerializer(lesson)
        return Response(ser.data)
    
    def post(self,request):
        self.check_object_permissions(request,request.data)
        ser=LessonModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
    def put(self,request,lesson_id):
        
        lesson=get_object_or_404(LessonModel,id=lesson_id)
        ser=LessonModelSerializer(instance=lesson,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
    def delete(self,request,lesson_id):
    
        lesson=get_object_or_404(LessonModel,id=lesson_id)
        lesson.delete()
        return Response({'message':'Item Deleted Successfully!'})
    
class Get_All_Lesson_Via_Course(APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,(IsStudentCanManageOwnEnrollement|IsInstructorCreateupdatedeletelessons|IsAdmin)]
        
    def get(self,request,course_id):
        lessons=LessonModel.objects.filter(course=course_id)
        ser=LessonModelSerializer(lessons,many=True)
        return Response(ser.data)
    
    
    