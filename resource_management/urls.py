from django.urls import path
from . import views

app_name = 'resource_management'

urlpatterns = [
    # Student Views
    path('view/question-papers/', views.view_question_papers, name='view_question_papers'),
    path('view/timetables/', views.view_timetables, name='view_timetables'),  # ✅ added this
    path('view/timetables/<int:pk>/', views.view_timetable_file, name='view_timetable_file'),

    # Uploads
    path('upload/question-paper/', views.upload_question_paper, name='upload_question_paper'),
    path('upload/timetable/', views.upload_timetable, name='upload_timetable'),

    # Student Resources / Notifications
    path('student/resources/', views.student_resources, name='student_resources'),
    path('notifications/', views.notifications, name='notifications'),
    path('view_notifications/', views.view_notifications, name='view_notifications'),
]

