from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from tests.models import Order, User 
from django.views.decorators.cache import never_cache
from tests.models import Appoinment, Patient, Test, User, Address, Location, Payment, Review,Report,Product
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Avg
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse
#superuser accessed condition
def is_superuser(user):
    return user.is_superuser


@never_cache
@login_required(login_url='login')
def staff_dashboard(request):
    context = {}  # Create an empty context

    if request.user.is_staff and not request.user.is_superuser:
        # Fetch recent appointments edited by the logged staff
        recent_appointments = Appoinment.objects.filter(
            Q(user=request.user) | Q(report__uploaded_by=request.user)
        ).order_by('-updated_at')[:5]  # Adjust the number of appointments as needed

        context["recent_appointments"] = recent_appointments

        return render(request, "staff_dashboard.html", context)
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

@never_cache
@login_required(login_url='login')
def staff_applist(request):
    # Query the database to get all appointments
    appointments = Appoinment.objects.filter(payment__status=True).order_by('-created_at')
    
    # Pass the appointments to the template
    context = {
        'appointments': appointments,
    }
    return render(request, 'staff_applist.html', context)

@never_cache
@login_required(login_url='login')
def staff_edit(request):
    appointment_id = request.GET.get("appointmentId")
    appointment = get_object_or_404(Appoinment, id=appointment_id)

    if request.method == "POST":
        # Assuming you have an 'update_appointment' function to handle the form submission
        update_appointment(request)

        # Add a success message
        messages.success(request, "Appointment updated successfully.")

        # Redirect back to the staff_edit page with the updated information
        return redirect('staff_edit', appointmentId=appointment_id)

    context = {
        "appointment": appointment,
    }

    return render(request, "staff_edit.html", context)

@never_cache
@login_required(login_url='login')
def update_appointment(request):
    if request.method == "POST":
        appoinment_id = request.POST.get("appoinment_id")
        appointment_status = request.POST.get("appointment_status")
        result_file = request.FILES.get("result_upload")  # Corrected spelling
        print(f"Appointment ID: {appoinment_id}")
        print(f"Appointment Status: {appointment_status}")
        print(f"Result File: {result_file}")
        try:
            # Get the appointment instance
            appointment = Appoinment.objects.get(id=appoinment_id)

            # Update appointment status
            appointment.appointment_status = appointment_status

            # Update report if a file is uploaded
            if result_file:
                # Create or update the report
                report, created = Report.objects.get_or_create(appoinment=appointment)
                report.result_file = result_file
                report.uploaded_by = request.user
                report.save()
               
                appointment.report = report
            # Save changes
                
            appointment.save()
            messages.success(request, "Appointment updated successfully.")
        except Appoinment.DoesNotExist:
            messages.error(request, "Appointment not found.")
        except Exception as e:
            messages.error(request, f"Error updating appointment: {str(e)}")

        return redirect("staff_applist")  # Replace with the actual URL you want to redirect to

    # Handle the case when the request method is not POST
    return HttpResponse("Invalid request method")

@never_cache
@login_required(login_url='login')
def addproduct(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_price = Decimal(request.POST['product_price'])
        brand = request.POST['brand']
        is_available = request.POST.get('is_available')  # Get the checkbox value

        # If the checkbox is not checked, set is_available to False
        if is_available is None:
            is_available = False
        else:
            is_available = True

        product_image = request.FILES['product_image'] if 'product_image' in request.FILES else None
        discount = Decimal(request.POST['discount'])
        
        # Ensure product_sale_price is a Decimal for precise calculations
        # product_sale_price = product_price - (product_price * (discount / 100))

        stock = int(request.POST['stock'])
        description = request.POST['description'] 

        # Save the product to the database
        product = Product(
            product_name=product_name,
            product_price=product_price,
            brand=brand,
            is_available=is_available,
            product_image=product_image,
            discount=discount,
            stock=stock,
            description=description,  
        )
        product.save()
    

        messages.success(request, 'Health product added successfully.')
        return redirect('adminproduct.html')  # Adjust the URL as needed

    return render(request, "addproduct.html")

@never_cache
@login_required(login_url='login')
def adminproduct(request):
    # Fetch all products from the database
    products = Product.objects.all()

    # Pass the products to the template context
    context = {
        'products': products,
    }

    return render(request, "adminproduct.html", context)

@never_cache
@login_required(login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        brand = request.POST.get('brand')
        is_available = request.POST.get('is_available')
        product_image = request.FILES.get('product_image') if 'product_image' in request.FILES else None
        discount = request.POST.get('discount')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        # Update the product attributes
        product.product_name = product_name
        product.product_price = product_price
        product.brand = brand
        product.is_available = True if is_available == 'on' else False
        if product_image:
            product.product_image = product_image
        product.discount = discount
        product.stock = stock
        product.description = description 
        product.save()
        messages.success(request, 'product details updated successfully.')
        return redirect('adminproduct')  # Redirect to the product list page after saving changes
    
    return render(request, 'updateproduct.html', {'product': product})

@never_cache
@login_required(login_url='login')
def delete_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(pk=product_id)
            product.is_available = False
            product.save()
            messages.success(request, 'Product deleted successfully.')
        except Product.DoesNotExist:
            messages.error(request, 'Product not found.')
        
    return redirect('adminproduct')  # Redirect to the product list page after deletion

@never_cache
@login_required(login_url='login')
def adddeliveryboy(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST["first-name"]
        email = request.POST['email']
        # Create the user and set is_staff to True
        user = User.objects.create_user(username=username, password=password)
        user.is_deliveryboy = True
        user.first_name = first_name
        user.email=email
        user.save()

        # Log in the new staff member
        send_mail(
            'Welcome to OneHealth',
            f'Dear {first_name},\n\nYou have been added as a staff member.Your username is {username} and your password is {password}.\n\nPlease keep your credentials secure.',
            'your_email@example.com',  # Replace with your email address
            [email], 
            fail_silently=False,
        )
        messages.success(request, "Delivery Boy is added successfully.")
        return redirect('admin_dashboard')  # Redirect to staff_dashboard

    return render(request, 'add_deliveryboy.html')

@never_cache
@login_required(login_url='login')
def deliveryboy_dashboard(request):
    return render(request, "deliveryboy_dashboard.html")

@never_cache
@login_required(login_url='login')
def order_deliverboy(request):
    orders = Order.objects.order_by('-id')[:5]
    return render(request, 'order_deliverboy.html', {'orders': orders})

@never_cache
@login_required(login_url='login')
def admindeliveryboy(request):
    staff_users = User.objects.filter(is_deliveryboy=True,is_staff=False,is_superuser=False)
    context = {'staff_users': staff_users}
    return render(request, 'admindeliveryboy.html', context)

@never_cache
@login_required(login_url='login')
@user_passes_test(is_superuser)
def delete_deliveryboy(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_deliveryboy = False
    user.is_active = False
    user.save()
    messages.success(request, "Delivery boy is removed successfully.")
    return redirect('admin_dashboard') 

@never_cache
@login_required(login_url='login')
def deliveryboy_edit(request):
    return render(request, "deliveryboy_edit.html")
