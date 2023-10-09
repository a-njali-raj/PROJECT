from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

from tests.models import (
    Address,
    Test,
    Patient,
    Appoinment,
)

User = get_user_model()

@never_cache
def index(request):
    return render(request, "index.html")

@never_cache
def about(request):
    return render(request, "about.html")

@never_cache
@login_required
def services(request):
    context = {
        "tests": Test.objects.filter(is_available=True),
    }
    return render(request, "services.html", context)

@never_cache
def contact(request):
    return render(request, "contact.html")

@never_cache
def loginn(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username']=user.username
            if user.is_superuser:
                messages.success(request, "Login successful.")
                return redirect("admin_dashboard")
            elif user.is_staff:
                return redirect("staff_dashboard")
            messages.success(request, "Login successful.")
            return redirect("user")
            
        else:
            messages.error(
                request, "Invalid username or password"
            )  # Add an error message
            return redirect("login")  # Redirect back to the login page

    response = render(request,"login.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response

@never_cache
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        first_name = request.POST["first-name"]
        phone_number = request.POST["phone"]
        street_address = request.POST["home"]
        city = request.POST["city"]
        pincode = request.POST["zip"]
        address = Address.objects.create(
            street_address=street_address,
            city=city,
            pincode=pincode,
        )
        User.objects.create_user(
            username,
            email,
            password,
            first_name=first_name,
            phone_number=phone_number,
            address=address,
        )
        messages.success(request, "registration successful.")
        return redirect("login")
    return render(request, "signup.html")

def check_username_availability(request):
    if request.method == "GET":
        username = request.GET.get("username")

        try:
            user = User.objects.get(username=username)
            available = False
        except User.DoesNotExist:
            available = True

        return JsonResponse({"available": available})

def check_email_availability(request):
    email = request.GET.get('email', '')

    if len(email) >= 5:  # Adjust the minimum length as needed
        # Check if the email exists in your database
        user = User.objects.filter(email=email).first()

        if user:
            return JsonResponse({'available': False})  # Email is already registered
        else:
            return JsonResponse({'available': True})  # Email is available
    else:
        return JsonResponse({'available': False})  # Emai
@never_cache
@login_required
def appoinment(request):
    context = {
        "tests": Test.objects.filter(is_available=True),
    }
    if request.method == "POST":
        print(request.POST)
        patients = []
        additional_test = None
        # Parsing data from payload
        test = request.POST["test"]
        preffered_date = request.POST["date"]
        preffered_time = request.POST["preferred-time"]
        patient_count = request.POST["persons"]
        patient_count = int(patient_count) if patient_count else 0
        email = request.POST["email"]
        phone = request.POST["phone"]
        address_choice = request.POST["address-choice"]
        additional_test_id = request.POST.get("additional_tests_select")
        appoinment_type = request.POST["appointmentType"]

        # Getting main test object
        main_test = Test.objects.get(pk=test)
        # Getting additional test object if additional test id is selected
        if additional_test_id:
            additional_test = Test.objects.get(pk=additional_test_id)
        if address_choice == "current-address":
            # Getting users address
            address = request.user.address
        else:
            # Creating address from payload
            street_address = request.POST.get("new-home-address")
            city = request.POST.get("new-city")
            pincode = request.POST.get("new-pincode")
            address = Address.objects.create(
                street_address=street_address,
                city=city,
                pincode=pincode,
            )

        # Creating patient instances from payload
        for i in range(1, patient_count + 1):
            patient_name = request.POST.get(f"name{i}")
            patient_age = request.POST.get(f"age{i}")
            patient_gender = request.POST.get(f"gender{i}")
            patients.append(
                Patient.objects.create(
                    full_name=patient_name,
                    age=patient_age or None,
                    gender=patient_gender or None,
                )
            )

        # Creating appoinment instance
        _appoinment = Appoinment.objects.create(
            main_test=main_test,
            preffered_date=preffered_date,
            preffered_time=preffered_time,
            email=email,
            phone_number=phone,
            address=address,
            additional_test=additional_test,
            appoinment_type=appoinment_type,
            user=request.user,
        )

        # Setting patients to appoinment instance
        if patients:
            _appoinment.patients.add(*patients)

        messages.success(request, "Appoinment created successfully.")

        return redirect("/")

    return render(request, "appoinment.html", context)
@never_cache
@login_required(login_url='login')
def user(request):
      if 'username' in request.session:
        response = render(request,"user.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
      else:
        return redirect("login.html")

@never_cache
def logout(request):
    auth.logout(request)
    return redirect("/")

@never_cache
def services1(request):
    return render(request, "services1.html")
@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
