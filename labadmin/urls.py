
from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('staff-dashboard',views.staff_dashboard, name="staff_dashboard"),
    path('admin-dashboard',views.admin_dashboard, name="admin_dashboard"),
    path('userdetails.html',views.userdetails, name="userdetails"),
    path('admintest.html',views.admintest, name="admintest"),
    path('addtest.html', views.addtest, name="addtest"),
    path('updatetest.html', views.updatetest, name="updatetest"),
    path('delete_test/<int:test_id>/', views.delete_test, name='delete_test'),
    path('adminstaff.html', views.adminstaff, name="adminstaff"),
    path('addstaff.html', views.addstaff, name="addstaff"),
    path('delete_staff/<int:user_id>/', views.delete_staff, name='delete_staff'),
    path('stafftest.html', views.stafftest, name="stafftest"),
    path('appoinmentlist.html',views.appoinmentlist,name="appoinmentlist"),
    path('appdetaillist.html',views.appdetaillist,name="appdetaillist"),
    path('staff_applist.html',views.staff_applist,name="staff_applist"),
    path('staff_edit.html',views.staff_edit,name="staff_edit"),
    
]

