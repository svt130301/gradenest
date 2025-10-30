from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # User Management
#    path('users/', views.user_list, name='user_list'),
 #   path('users/add/', views.add_user, name='add_user'),
  #  path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    # Program Management
    path('programs/', views.program_list, name='program_list'),
    path('programs/add/', views.add_program, name='add_program'),
    path('programs/delete/<int:program_id>/', views.delete_program, name='delete_program'),

    # Subject Management
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    path('subjects/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),

    # Faculty Assignment
    path('faculty/assign/', views.assign_faculty, name='assign_faculty'),
]
