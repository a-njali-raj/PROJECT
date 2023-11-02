from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
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
        users = User.objects.filter(is_superuser=False, is_staff=False)
        return render(request, "admin_dashboard.html", {"users": users})
    return redirect("home")
@never_cache
@login_required(login_url='login')
def userdetails(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser=False, is_staff=False)
        return render(request, "userdetails.html", {"users": users})
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
        is_available = request.POST.get('is_available')  # Get the checkbox value

        # If the checkbox is not checked, set is_available to False
        if is_available is None:
            is_available = False
        else:
            is_available = True

        if name and price:
            Test.objects.create(name=name, price=price, is_available=is_available)
            return redirect("admintest")  # Redirect to a success page or any other page
    return render(request, "addtest.html")

def delete_test(request,test_id):
    test = get_object_or_404(Test, id=test_id)

    # Instead of deleting, change the availability status to False
    test.is_available = False
    test.save()

    return redirect("admintest")
@never_cache
@login_required(login_url='login')
def updatetest(request):
    # Retrieve 'test_id' from the query parameter 'test_id'
    test_id = request.GET.get('test_id')

    if request.method == 'POST':
        # Get the updated data from the form
        name = request.POST.get('name')
        price = request.POST.get('price')
        availability = request.POST.get('availability')

        # Retrieve the test instance based on the 'test_id'
        test = Test.objects.get(pk=test_id)

        # Update the test's attributes
        test.name = name
        test.price = price
        test.is_available = availability == "True"  # Convert to boolean

        # Save the updated test
        test.save()

        # Redirect to a success page or return a response
        return redirect('admintest')  # Replace 'success_page' with the appropriate URL

    # Handle GET requests for editing the test details
    else:
        # Retrieve the test instance based on the 'test_id'
        test = Test.objects.get(pk=test_id)
        context = {
            'test': test,
        }
        return render(request, "updatetest.html", context)
@never_cache
def adminstaff(request):
    return render(request, "adminstaff.html")
@never_cache
def addstaff(request):
    return render(request, "addstaff.html")
