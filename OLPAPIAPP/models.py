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