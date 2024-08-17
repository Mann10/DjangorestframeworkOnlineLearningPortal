from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUserModel(AbstractUser):
    unique_person_id=models.CharField(max_length=200,null=True,blank=True)
    role=models.CharField(max_length=50,choices=[('student','STUDENT'),('instructor','Instructor'),('admin','Admin')])
    profile_picture=models.ImageField(upload_to='profile_pictures/',blank=True,null=True)
    bio=models.CharField(max_length=250)
    
    # def __str__(self) -> str:
    #     return f'{self.username} + {self.profile_picture}'
    
    def __str__(self) -> str:
        return f'{self.username}'
    