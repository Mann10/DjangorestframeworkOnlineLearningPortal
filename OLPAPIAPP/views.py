from django.shortcuts import render,get_object_or_404
from django.utils import timezone
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
    
    
class ProgressModelView(APIView):
    def post(self,request):
        print(f'Before printing the progess--{request.data}')
        progress=ProgressModelSerializer(data=request.data)
        print(f'After printing data--{progress.initial_data}')
       
        if progress.is_valid():
            course_id=progress.validated_data['course'].id
            course=CourseModel.objects.get(id=course_id)
            Number_of_lessons_in_each_course=int(course.lesson_course.count())
            progress.validated_data['percentage_completed']=(1/Number_of_lessons_in_each_course)*100
            progress.save()
            return Response(progress.data)
        return Response(progress.errors)  
    
class ProgressModelDetail(APIView):
    
    def get(self,request,progress_id):
        progress_details=get_object_or_404(ProgressModel,id=progress_id)
        ser=ProgressModelSerializer(progress_details)
        return Response(ser.data) 
       
    def put(self,request,progress_id):
        print(progress_id)
        progress_data=get_object_or_404(ProgressModel,id=progress_id)
        print(progress_data)
        ser=ProgressModelSerializer(data=request.data,instance=progress_data)
        print(ser.initial_data)
        print(progress_data.is_completed)
        if progress_data.is_completed==False:
            if ser.is_valid():
                print(ser.validated_data)
                course_id=ser.validated_data['course'].id
                print(course_id)
                course=CourseModel.objects.get(id=course_id)
                print(course)
                Number_of_lessons_in_each_course=int(course.lesson_course.count())
                print(Number_of_lessons_in_each_course)
                print(f'current_lesson-{ser.validated_data['current_lesson'].id}')
                completed_course=course.lesson_course.filter(id__lte=ser.validated_data['current_lesson'].id).count()
                print(completed_course)
                ser.validated_data['percentage_completed']=(completed_course/Number_of_lessons_in_each_course)*100
                ser.save()
                return Response(ser.data)
            return Response(ser.errors)
        else:
            return Response('You have completed this module,cheers up!')
        
class CreateQuiz(APIView):
    def get(self,request):
        quizes=QuizModel.objects.all()
        ser=CreateQuizModelSerializer(quizes,many=True)
        return Response(ser.data)
        
        
    def post(self,request):
        ser=CreateQuizModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
class QuizDetailView(APIView):
    
    def get(self,request,quiz_id):
        quiz=get_object_or_404(QuizModel,id=quiz_id)
        ser=CreateQuizModelSerializer(quiz)
        return Response(ser.data)
        
class QuestionView(APIView):
    
    def get(self,request):
        questions=QuestionModel.objects.all()
        ser=QuestionSerializer(questions,many=True)
        for dic in ser.data:
            for key,value in dic.copy().items():
                if key=='question':
                    del dic[key]
        return Response(ser.data)
    
    def post(self,request):
        ser=QuestionSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
class QuestionDetailView(APIView):
    def get(self,request,quiz_id):
        questions_for_perticuale_quiz=QuestionModel.objects.filter(quiz=quiz_id)
        ser=QuestionSerializer(questions_for_perticuale_quiz,many=True)
      
        for dic in ser.data:
            for key,value in dic.copy().items():
                if key=='question':
                    del dic[key]
        return Response(ser.data)

class QuestionAlongAnswerView(APIView):
    def get(self,request,question_id):
        question=get_object_or_404(QuestionModel,id=question_id)
        ser=QuestionSerializer(question)
        return Response(ser.data)

class AnswerView(APIView):
    
    def post(self,request):
        ser=AnswerSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)  
       
class AnswerDetailView(APIView):
    
    def get(self,request,question_id):
        try:
            answers=AnswerModel.objects.filter(question=question_id)
        except AnswerModel.DoesNotExist:
            return Response("Matching question id dosen't exists")
        ser=AnswerSerializer(answers,many=True)
        return Response(ser.data)
        
        
class SubmitQuizView(APIView):
    
    def post(self,request,quiz_id):
        quiz=get_object_or_404(QuizModel,id=quiz_id)
        storing_updated_result=ResultModel()
        storing_updated_result.quiz=quiz
        storing_updated_result.user_id=request.user.id
        storing_updated_result.user_id=1
        storing_updated_result.score=0
        for elem in request.data.get('answers'):
            question=quiz.questions.get(id=elem.get('question_id'))
            if question.question_type in ['mcq','true/false']:  
                answer=question.question.get(id=elem.get('answer_id'))
                if answer.is_correct:
                    storing_updated_result.score=storing_updated_result.score+1           
            else:
                is_completed_list_for_msq=question.question.filter(id__in=elem.get('answer_id')).values_list('is_correct',flat=True)
                correct_answers=question.question.filter(is_correct=True)
                
                if is_completed_list_for_msq.count()==correct_answers.count() and all(x for x in is_completed_list_for_msq):
                    storing_updated_result.score=storing_updated_result.score+1
                    
        que=quiz.questions.filter(quiz_id=quiz_id).count()       
        pass_threshold=que//2
        
        if storing_updated_result.score >=pass_threshold:
            storing_updated_result.passed=True
        else:
            storing_updated_result.passed=False
        
        storing_updated_result.completed_at=timezone.now()
        storing_updated_result.save()
        if storing_updated_result.passed:
            return Response(f'Congrates you have passed examination with score : {storing_updated_result.score} at {storing_updated_result.completed_at}.')
        return Response(f'oops you failed with score : {storing_updated_result.score} at {storing_updated_result.completed_at}.')
                    
class QuizResultView(APIView):
    
    def get(self,request,user_id):
        result=ResultModel.objects.filter(user=user_id)
        ser=ResultModelSerializer(result,many=True)
        return Response(ser.data)                
                
                    
                
         