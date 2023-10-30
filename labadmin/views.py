from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tests.models import User 
from django.views.decorators.cache import never_cache
@never_cache
@login_required(login_url='login')
def staff_dashboard(request):
    if request.user.is_staff and not request.user.is_superuser:
        
        return render(request, "staff_dashboard.html")
    return redirect("home")

@never_cache
@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.is_superuser:
        users = User.objects.exclude(is_superuser=True)# Query the registered users
        return render(request, "admin_dashboard.html", {"users": users})  # Pass 'users' to the template context
    return redirect("home")
@never_cache
@login_required(login_url='login')
def userdetails(request):
    if request.user.is_superuser:
        users = User.objects.exclude(is_superuser=True)# Query the registered users
        return render(request, "userdetails.html", {"users": users})  # Pass 'users' to the template context
    return redirect("home")
   
@never_cache
def admintest(request):
    return render(request, "admintest.html")