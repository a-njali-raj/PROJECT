
from django.contrib import admin
from django.urls import path
from.import views


urlpatterns = [
    path('',views.index,name="home"),
    path('index.html',views.index,name="home"),
    path('about.html',views.about,name="about"),
    path('services.html',views.services,name="services"),
    path('contact.html',views.contact,name="contact"),
    path('login.html',views.loginn,name="login"),
    path('signup.html',views.signup,name="signup"),
    path('appoinment.html',views.appoinment,name="appoinment"),
    path('user.html',views.user,name="user"),
    path('logout/',views.logout,name="logout"),
    path('services1.html',views.services1,name="services1"),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('check_phone/', views.check_phone, name='check_phone'),
]
