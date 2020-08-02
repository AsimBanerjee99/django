"""time_table URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login_func, name='login'),
    path('logout/', views.logout_func, name='logout'),
    path('createtimetable/', views.createtimetable, name='createtimetable'),
    path('remove_row/', views.remove_row, name='remove_row'),
    path('remove_column/', views.remove_column, name='remove_column'),
    path('remove_table/', views.remove_table, name='remove_table'),

]