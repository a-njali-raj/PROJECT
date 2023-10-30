
from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('staff-dashboard',views.staff_dashboard, name="staff_dashboard"),
    path('admin-dashboard',views.admin_dashboard, name="admin_dashboard"),
    path('userdetails.html',views.userdetails, name="userdetails"),
    path('admintest.html',views.admintest, name="admintest"),
    path('addtest.html', views.addtest, name="addtest"),
]

