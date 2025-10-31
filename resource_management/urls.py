from django.urls import path
from . import views

app_name = 'resource_management'

urlpatterns = [
    path('view/question-papers/', views.view_question_papers, name='view_question_papers'),
    path('view/timetables/', views.view_timetables, name='view_timetables'),
    path('upload/question-paper/', views.upload_question_paper, name='upload_question_paper'),
    path('upload/timetable/', views.upload_timetable, name='upload_timetable'),
    path('student/resources/', views.student_resources, name='student_resources'),
    path('notifications/', views.notifications, name='notifications'),
    path('view_notifications/', views.view_notifications, name='view_notifications'),
]

