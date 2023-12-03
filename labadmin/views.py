from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from tests.models import User 
from django.views.decorators.cache import never_cache
from tests.models import Appoinment, Patient, Test, User, Address, Location, Payment, Review
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg
from django.http import JsonResponse
#superuser accessed condition
def is_superuser(user):
    return user.is_superuser


@never_cache
@login_required(login_url='login')
def staff_dashboard(request):
    if request.user.is_staff and not request.user.is_superuser:
        
        return render(request, "staff_dashboard.html")
    return redirect("home")

@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
def admin_dashboard(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser=False)
       # Get the count of reviews and average rating
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']

        return render(request, "admin_dashboard.html", {"users": users, "review_count": review_count, "average_rating": average_rating})
    return redirect("home")
@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
def userdetails(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
        return render(request, "userdetails.html", {"users": users})
    return redirect("home")
   
@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
def admintest(request):
    tests = Test.objects.all() 
    return render(request, "admintest.html", {'tests': tests}) # Retrieve all Test objects from the database

@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
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
            messages.success(request, "Test  added successfully.")
            return redirect("admintest")  # Redirect to a success page or any other page
    return render(request, "addtest.html")

@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
def delete_test(request,test_id):
    test = get_object_or_404(Test, id=test_id)

    # Instead of deleting, change the availability status to False
    test.is_available = False
    test.save()
    messages.success(request, "test deleted successfully.")
    return redirect("admintest")

@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
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
        messages.success(request, "Test updated successfully.")
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
@login_required(login_url='login')
@user_passes_test(is_superuser)
def adminstaff(request):
    staff_users = User.objects.filter(is_staff=True,is_superuser=False)
    context = {'staff_users': staff_users}
    return render(request, 'adminstaff.html', context)


@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
def addstaff(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST["first-name"]
        email = request.POST['email']
        # Create the user and set is_staff to True
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.first_name = first_name
        user.email=email
        user.save()

        # Log in the new staff member
        send_mail(
            'Welcome to OneHealth',
            f'Dear {first_name},\n\nYou have been added as a staff member.Your username is {username} and your password is {password}.\n\nPlease keep your credentials secure.',
            'your_email@example.com',  # Replace with your email address
            [email],  # Use the staff member's email address
            fail_silently=False,
        )
        messages.success(request, "Staff is added successfully.")
        return redirect('admin_dashboard')  # Redirect to staff_dashboard

    return render(request, 'addstaff.html')

@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
def delete_staff(request, user_id):
    # Get the user object to delete
    user = get_object_or_404(User, id=user_id)

    # Set is_staff status to 0
    user.is_staff = False
    user.is_active = False
    user.save()

    # You can add a confirmation message if needed
    messages.success(request, "staff is removed successfully.")

    # Redirect to a staff list page or wherever you need to go
    return redirect('admin_dashboard')  # Replace 'staff_list' with the actual URL name for your staff list page

@never_cache
@login_required(login_url='login')
def stafftest(request):
    tests = Test.objects.all() 
    return render(request, "stafftest.html", {'tests': tests}) # Retrieve all Test objects from the database
@never_cache
@login_required(login_url='login')
def appoinmentlist(request):
    # Query the database to get all appointments
    appointments = Appoinment.objects.filter(payment__status=True).order_by('-created_at')
    
    # Pass the appointments to the template
    context = {
        'appointments': appointments,
    }
    
    return render(request, 'appoinmentlist.html', context)
@never_cache
@login_required(login_url='login')
def appdetaillist(request):
    appointment_id = request.GET.get('appointmentId')

    # Retrieve the appointment details or return a 404 error if not found
    appointment = get_object_or_404(Appoinment, id=appointment_id)

    # Customize this part based on your model structure
    appointment_details = {
        'patient_names': [patient.full_name for patient in appointment.patients.all()],
        'object_id': appointment.object_id,
        'main_test': appointment.main_test.name if appointment.main_test else None,
        'preferred_date': appointment.preffered_date,
        'preferred_time': appointment.preffered_time,
        'email': appointment.email,
        'phone_number': appointment.phone_number,
        'address': appointment.address.street_address if appointment.address else None,
        'additional_test': appointment.additional_test.name if appointment.additional_test else None,
        'appointment_type': appointment.appoinment_type,
        'prescription_file': appointment.prescription if appointment.prescription else None,

        'location': appointment.location.address if appointment.location else None,
        'amount': appointment.amount,
        
    }
    return render(request, 'appdetaillist.html', {'appointment_details': appointment_details})