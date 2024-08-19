from rest_framework.permissions import BasePermission
from .models import CourseModel
from rest_framework import permissions

class IsStudentAndReadOnlyCourses(BasePermission):
    def has_permission(self, request, view):
    
        if request.user.role=='student' and request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
        
class IsStudentCanManageOwnEnrollement(BasePermission):
    
    def has_permission(self, request, view):
        print("Checking general permission...")
        if request.user.role=='student' and request.method in ['POST','GET','DELETE']:
            print("General permission granted.")
            return True
        else:
            print("General permission denied.")
            return False
        
    def has_object_permission(self, request, view, obj):
        print("Checking object permission for DELETE...")
        if request.user.role=='student' and  request.method in ['GET','DELETE']:
            print(f"Object: {obj}, User: {request.user}")
            return obj.user==request.user  # checking if obj fetched from database thorugh id we got and logged in user are same or not.
        print("Object permission denied.")
        print(f"Object: {obj}, User: {request.user}")
        print(obj)
        return False
    
     
class IsIntructorCanCreateUpdateDestroyCourse(BasePermission):
    '''
    This Class will alow instructors to get all other instructors course and post or create there own course and can only update and delete there own course.
    '''
    def has_permission(self, request, view):
        print("Checking general permission...")
        if request.user.role=='instructor':
            
            if request.method in permissions.SAFE_METHODS or request.method=='POST':
                print("General permission granted. for get and post")
                return True
            elif request.user.role=='instructor' and request.method in ['PUT','DELETE']: # This will allow any instructor to update or delete any instructors course. To avoid this we will call has_object_permission.
                print("General permission granted. for 'PUT','DELETE'")
                return True
            else:
                print("General permission denied.")
                return False
        return False
    
    def has_object_permission(self, request, view, obj):
        print("Checking object permission for 'PUT','DELETE'...")
        if request.user.role=='instructor' and request.method in ['PUT','DELETE']:
            print(f"Object: {obj}, User: {request.user}")
            return obj.instructor==request.user
        print("Object permission denied.")
        return False    
    

class IsInstructorCreateupdatedeletelessons(BasePermission):
    '''
    This is custom permission so that only Intructor who created the course can add update or delete lessons.
    '''
    
    def has_permission(self, request, view):
        if request.user.role=='instructor' and (request.method==permissions.SAFE_METHODS or request.method in ['POST','PUT''DELETE']):
            return True
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.role=='instructor' and request.method in ['POST','PUT''DELETE']:
            course_obj=CourseModel.objects.get(id=int( obj['course']))
            print(obj)
            return course_obj.instructor==request.user
        return False
        
class IsAdmin(BasePermission):
    
    '''
    This is for admin level permission and they can do anything in this project which includes,
    crud operations for cources,lessons, enrollments etc.
    '''
    def has_permission(self, request, view):
        if request.user.role=='admin' and request.user.is_staff:
            return True
        return False      
    