from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tests.models import User 
from django.views.decorators.cache import never_cache
from tests.models import Test
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
@login_required(login_url='login')
def admintest(request):
    tests = Test.objects.all() 
    return render(request, "admintest.html", {'tests': tests}) # Retrieve all Test objects from the database
@never_cache
@login_required(login_url='login')
def addtest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        
        if name and price:
            Test.objects.create(name=name, price=price)
            return redirect("admintest")  # Redirect to a success page or any other page

    return render(request, "addtest.html")
def updatetest(request):
    return render(request, "updatetest.html")