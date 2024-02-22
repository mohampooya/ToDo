from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from .views import profile_customization
from django.urls import re_path
from .views import create_task


urlpatterns = [
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('', views.main_page, name='main_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('tasks/', views.task_list, name='task_list'),
    path('task/update/<int:pk>/', views.update_task, name='update_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('create_list/', views.create_list, name='create_list'),
    path('create_task/', views.create_task, name='create_task'),
    path('profile/', profile_customization, name='profile_customization'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('lists/<int:list_id>/', views.view_list, name='view_list'),
    path('tasks/create/<int:list_id>/', views.create_task, name='create_task'),
    path('create_task/<int:list_id>/', create_task, name='create_task_with_list'),
    path('task/<int:task_id>/toggle/', views.toggle_task_status, name='toggle_task_status'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),

    #re_path(r'^create_task/(?P<list_id>\d+)?/$', views.create_task, name='create_task'),




    
]
