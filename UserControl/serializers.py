from rest_framework import serializers
from .models import CustomUserModel

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserModel
        fields=['first_name','last_name','username','password','email','role','profile_picture','bio']
        
class CustomLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserModel
        fields=['unique_person_id','password'] 
    

class CustomProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserModel
        fields=['unique_person_id','first_name','last_name','username','password','email','role','profile_picture','bio']
    