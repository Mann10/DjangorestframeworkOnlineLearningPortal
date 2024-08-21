from django.contrib import admin
from UserControl.models import *
from .models import *
# Register your models here.


admin.site.register(CustomUserModel)
admin.site.register(CourseModel)
admin.site.register(EnrollmentModel)
admin.site.register(LessonModel)
admin.site.register(ProgressModel)
admin.site.register(QuizModel)
admin.site.register(QuestionModel)
admin.site.register(AnswerModel)
admin.site.register(ResultModel)