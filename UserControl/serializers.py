from rest_framework import serializers
from .models import CustomUserModel
from OLPAPIAPP.serializers import CourseModelSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserModel
        fields=['first_name','last_name','username','password','email','role','profile_picture','bio']
        
class CustomLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUserModel
        fields=['unique_person_id','password'] 
    

class CustomProfileSerializer(serializers.ModelSerializer):
    #coursemodel=CourseModelSerializer(read_only=True,many=True)
    class Meta:
        model=CustomUserModel
        fields=['unique_person_id','first_name','last_name','username','password','email','role','profile_picture','bio']
    def to_representation(self, instance):
        from OLPAPIAPP.serializers import CourseModelSerializer # Local import to avoid circular dependency
        representation = super().to_representation(instance)
        representation['coursemodel'] = CourseModelSerializer(instance.coursemodel, many=True,read_only=True).data
        return representation