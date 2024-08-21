from django.urls import path,include
from .views import *

urlpatterns = [
    path('courses/',CourseCreateView.as_view(),name='courses'),
    path('courses/<int:course_id>/',CourseDetailView.as_view(),name='course-id'),
    path('courses/create/',CourseCreateView.as_view(),name='courses-create'),
    path('courses/<int:course_id>/update/',CourseDetailView.as_view(),name='course-update'),
    path('courses/<int:course_id>/delete/',CourseDetailView.as_view(),name='course-update'),
    path('enrollments/',EnrollmentCreateView.as_view(),name='enrollments'),
    path('courses/<int:course_id>/enroll/',EnrollmentCreateView.as_view(),name='course-enroll'),
    path('enrollments/<int:enrollment_id>/',EnrollmentDetailView.as_view(),name='enrollments-id'),
    path('enrollments/<int:enrollment_id>/delete/',CourseDetailView.as_view(),name='enrollments-delete'),
    path('courses/<int:course_id>/lessons/',Get_All_Lesson_Via_Course.as_view(),name='course-lesson'),
    path('lessons/<int:lesson_id>',LessonDetailCrudView.as_view(),name='lesson-id'),
    path('lessons/create/',LessonDetailCrudView.as_view(),name='lesson-create'),
    path('lessons/<int:lesson_id>/update/',LessonDetailCrudView.as_view(),name='lesson-update'),
    path('lessons/<int:lesson_id>/delete/',LessonDetailCrudView.as_view(),name='lesson-delete'),
    path('progress/',ProgressModelView.as_view(),name='progress'),
    path('progress/<int:progress_id>/',ProgressModelDetail.as_view(),name='progress--update'),
    path('quiz/create/',CreateQuiz.as_view(),name='quiz-create'),
    path('quiz/',CreateQuiz.as_view(),name='quiz'),
    path('quiz/<int:quiz_id>/',QuizDetailView.as_view(),name='quiz'),
    path('question/',QuestionView.as_view(),name='question'),
    path('question/create/',QuestionView.as_view(),name='create-question'),
    path('question/<int:quiz_id>/',QuestionDetailView.as_view(),name='question-id'),
    path('eachquestionanditsanswer/<int:question_id>/',QuestionAlongAnswerView.as_view(),name='eachquestionalongwithanswer'),
    path('answer/create/',AnswerView.as_view(),name='create-answer'),
    path('answer/<int:question_id>/',AnswerDetailView.as_view(),name='answer'),
    path('quiz/<int:quiz_id>/submit/',SubmitQuizView.as_view(),name='quiz-submit'),
    path('user/<int:user_id>/results/',QuizResultView.as_view(),name='result'),
    
]
