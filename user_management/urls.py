from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    #path('', views.user_list, name='user_list'),
    path('add/', views.add_user_choice, name='add_user_choice'),
    path('add/student/', views.student_register, name='student_register'),
    path('add/staff/', views.staff_register, name='staff_register'),
    path('<int:user_id>/make_hod/', views.make_hod, name='make_hod'),
    path('<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('', views.user_list, name='user_list'),
]

