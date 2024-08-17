from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import *
from .serializers import *
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated




# Create your views here.

class UserRegistraion(APIView):
    
    def get(self,request):
        users=CustomUserModel.objects.all()
        ser=CustomUserSerializer(users,many=True)
        new=ser.data[0]
        print(new)
        for key , value in new.items():
            print(f'{key}={value}')
        return Response(ser.data)
        
    def post(self,request):
        role_list=['student','instructor','admin']
        ser=CustomUserSerializer(data=request.data)
        if ser.is_valid():
            ser.validated_data['unique_person_id']=str(uuid.uuid4())[:10]
            ser.save()
            return Response(f'Congratualations you are successfully registered. Your unique user id id {ser.validated_data['unique_person_id']}')
        return Response(ser.errors)
                
class Login(APIView):
    
    def post(self,request):
        ser= CustomLoginSerializer(data=request.data)
        if ser.is_valid():
            unique_person_id=ser.validated_data['unique_person_id']
            password=ser.validated_data['password']
            try:
                user_obj=CustomUserModel.objects.get(unique_person_id=unique_person_id)
            except CustomUserModel.DoesNotExist:
                return Response('Invalide credentials!')
            if (user_obj is not None) and (user_obj.password==password):
                refresh = RefreshToken.for_user(user_obj)

                return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                                })
            return Response('Invalide credentials!')
        else:
            return Response(ser.errors)
        
class UserProfile(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user_profile=CustomUserModel.objects.get(id=self.request.user.id) #django server will get the user from jwt for us.
        ser= CustomProfileSerializer(user_profile)
        return Response(ser.data)
        
        
    def put(self,request):
        user_id=self.request.user.id
        try:
            user_details=CustomUserModel.objects.get(id=user_id)
        except CustomUserModel.DoesNotExist:
            return Response('User details not found!')
        # if user_details.unique_person_id is not None:
        #     return Response('You cannot update unique_id')
        print(request.data)
        request.data['unique_person_id']=user_details.unique_person_id #Nomatter if he pass unique id or not it will never get updated.
        ser=CustomProfileSerializer(data=request.data,instance=user_details)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        else:
            return Response(ser.errors)
        
        