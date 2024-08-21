from typing import Iterable
from django.db import models
from UserControl.models import CustomUserModel
from django.core.exceptions import ValidationError

class CourseModel(models.Model):
    title=models.CharField(max_length=250)
    description=models.CharField(max_length=250)
    instructor=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='coursemodel')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    price=models.FloatField()
    
    def save(self,*args, **kwargs):
        if self.instructor.role=='student':
            raise ValidationError("Student Cannot create a course")
        else:
            return super().save(*args, **kwargs)
        
    
    def __str__(self) -> str:
        return f'Course {self.title} is offered by {self.instructor.role} {self.instructor}'
    

class EnrollmentModel(models.Model):
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE,related_name='enrolled_user')
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name='enrolled_course')
    enrollment_date=models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'User {self.user} enrolled in course {self.course}'
    
class LessonModel(models.Model):
    title=models.CharField(max_length=250)
    content_type=models.CharField(max_length=50,choices=[('video','VIDEO'),('text','TEXT')])
    content_url=models.URLField(blank=True,null=True)
    text_content=models.TextField(blank=True,null=True)
    course=models.ForeignKey(CourseModel,on_delete=models.CASCADE,related_name='lesson_course')
    
    def save(self,*args, **kwargs):
        if self.content_type=='video':
            self.text_content=None
        else:
            self.content_url=None
            
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f'{self.title}'
    
class ProgressModel(models.Model):
    user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE,related_name='progess_for_user')
    course=models.ForeignKey(CourseModel, on_delete=models.CASCADE,related_name='progress_for_course')
    current_lesson=models.ForeignKey(LessonModel,on_delete=models.CASCADE,related_name='lesson')
    is_completed=models.BooleanField(default=True)
    percentage_completed=models.DecimalField(default=0,max_digits=5, decimal_places=2)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='user_and_course_unique_together')
        ]
                   
    def save(self,*args, **kwargs):
        if self.percentage_completed==100.00:
            self.is_completed=True
        return super().save(*args, **kwargs)
    
    
class QuizModel(models.Model):
    title=models.CharField(("Enter the name of the quiz."), max_length=150)
    course=models.ForeignKey(CourseModel, on_delete=models.CASCADE)
    description=models.TextField(("Enter the description for your quiz."))
    
    def __str__(self) -> str:
        return f'Name of the quiz is :- {self.title}'
    
class QuestionModel(models.Model):
    quiz=models.ForeignKey(QuizModel, on_delete=models.CASCADE,related_name='questions')
    text=models.CharField(("Enter your question"), max_length=150)
    question_type=models.CharField(("What's type of your question"), max_length=50,choices=[('mcq','Normal'),('true/false','TRUE/FALSE'),('msq','multiple-choice')])
    
    def __str__(self) -> str:
        return f'Questions is :- {self.text}'
    
class AnswerModel(models.Model):
    question=models.ForeignKey(QuestionModel, on_delete=models.CASCADE,related_name='question')
    text=models.CharField(("Enter your options.."), max_length=50)
    is_correct=models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.text} | {self.is_correct}'
    
class ResultModel(models.Model):
    user=models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    quiz=models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    score=models.IntegerField()
    passed=models.BooleanField()
    completed_at=models.DateTimeField(auto_now=False, auto_now_add=False)