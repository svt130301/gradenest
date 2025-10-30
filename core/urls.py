from django.urls import path
from . import views

urlpatterns = [
    # PROGRAM URLs
    path('programs/', views.program_list, name='program_list'),
    path('programs/add/', views.program_add, name='program_add'),
    path('programs/edit/<int:pk>/', views.program_edit, name='program_edit'),
    path('programs/delete/<int:pk>/', views.program_delete, name='program_delete'),

    # SUBJECT URLs
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/edit/<int:pk>/', views.subject_edit, name='subject_edit'),
    path('subjects/delete/<int:pk>/', views.subject_delete, name='subject_delete'),
]
