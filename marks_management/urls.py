from django.urls import path
from . import views,views_office

app_name = 'marks_management'

urlpatterns = [
    path("enter-external-marks/", views.enter_external_marks, name="enter_external_marks"),
    path('office/select/', views_office.select_program_semester, name='select_program_semester'),
    path('office/enter/<int:program_id>/<int:semester>/', views_office.enter_external_marks, name='enter_external_marks'),
    path('office/enter/<int:program_id>/<int:semester>/<str:academic_year>/', views_office.enter_external_marks, name='enter_external_marks_year'),
    path('office/view-results/<int:program_id>/<int:semester>/', views_office.view_external_results, name='view_external_results'),
]

