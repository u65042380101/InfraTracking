"""
URL configuration for sak_infratrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/internet-links/<str:branch_code>/', views.internet_links_api, name='internet_links_api'),
    path('helpdesk-record/<str:branch_code>/', views.helpdesk_record, name='helpdesk_record'),
    path('add-record/', views.add_record, name='add_record'),
    path('edit-record/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete-record/<int:pk>/', views.delete_record, name='delete_record'),
    path('api/branch-info/', views.branch_info_api, name='branch_info_api'),
    path('summary-report/', views.summary_report, name='summary_report'),
]
