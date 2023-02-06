"""Myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CEO import views



urlpatterns = [
    
    path('home/', views.home, name='home'), 
    path('mhome/', views.mhome, name='mhome'),   
    path('ehome/', views.ehome, name='ehome'),    
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('c_profile/', views.c_profile, name='c_profile'), 
    path('m_profile/', views.m_profile, name='m_profile'),
    path('e_profile/', views.e_profile, name='e_profile'),       
    path('add_manager/',views.add_manager,name='add_manager'),
    path('add_employee/',views.add_employee,name='add_employee'),
    path('all_manager/',views.all_manager,name='all_manager'),
    path('all_employee/',views.all_employee,name='all_employee'),      
    path('edit/<str:id>/', views.edit, name='edit'),
    path('del_task/<str:id>/', views.del_task, name='del_task'),
    path('m_del_task/<str:id>/', views.m_del_task, name='m_del_task'),
    path('e_del_task/<str:id>/', views.e_del_task, name='e_del_task'),
    path('eedit/<str:id>/', views.eedit, name='eedit'),
    path('task/', views.task, name='task'), 
    path('mtask/', views.mtask, name='mtask'), 
    path('etask/', views.etask, name='etask'), 
    path('add_task/', views.add_task, name='add_task'), 
    path('c_edittask/<str:id>/', views.c_edittask, name='c_edittask'),
    path('m_edittask/<str:id>/', views.m_edittask, name='m_edittask'),
    path('e_edittask/<str:id>/', views.e_edittask, name='e_edittask'),
    path('add_message/', views.add_message, name='add_message'), 
    path('m_add_message/', views.m_add_message, name='m_add_message'), 
    path('e_add_message/', views.e_add_message, name='e_add_message'),
    path('all_message/', views.all_message, name='all_message'),
    path('m_all_message/', views.m_all_message, name='m_all_message'), 
    path('e_all_message/', views.e_all_message, name='e_all_message'), 
    path('edit_message/<str:id>/', views.edit_message, name='edit_message'),
    path('m_edit_message/<str:id>/', views.m_edit_message, name='m_edit_message'),
    path('e_edit_message/<str:id>/', views.e_edit_message, name='e_edit_message'),
    path('delete_message/<str:id>/', views.delete_message, name='delete_message'),
    path('m_delete_message/<str:id>/', views.m_delete_message, name='m_delete_message'),
    path('e_delete_message/<str:id>/', views.e_delete_message, name='e_delete_message'),
    
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('new_calendar/', views.new_calendar, name='new_calendar'),
	path('event_details/', views.event_details, name='event_details'),
    path('event/new/', views.create_event, name='event_new'),
    path('json', views.json, name='json'),
    

    

]
