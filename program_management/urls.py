from django.urls import path
from . import views
from .views import (
    program_list, program_add, program_edit, program_delete,
    subject_list, subject_add, subject_edit, subject_delete,
    assign_faculty, program_students, all_subjects
)

app_name = 'program_management'

urlpatterns = [
    path('', views.program_list, name='program_list'),
    path('add/', views.program_add, name='program_add'),
    path('<int:pk>/edit/', views.program_edit, name='program_edit'),
    path('<int:pk>/delete/', views.program_delete, name='program_delete'),

    path('subjects/', all_subjects, name='subject_list'),
    path('<int:program_id>/subjects/', views.subject_list, name='subject_list'),
    path('<int:program_id>/subjects/add/', subject_add, name='subject_add'),
    path('subjects/<int:pk>/edit/', subject_edit, name='subject_edit'),
    path('subjects/<int:pk>/delete/', subject_delete, name='subject_delete'),

    path('faculty/assign/', views.assign_faculty_dashboard, name='assign_faculty_dashboard'),

    path('subjects/<int:subject_id>/assign/', assign_faculty, name='assign_faculty'),
    path("promote/", views.promote_students, name="promote_students"),
    path('<int:program_id>/students/', program_students, name='program_students'),
]


