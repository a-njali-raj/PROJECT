from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from tests.models import (
    Address,
    Test,
    Patient,
    Appoinment,
    Location,
    Payment,
    Review,
)
from .razorpay import generate_order

User = get_user_model()

@never_cache
def index(request):
    reviews = Review.objects.all()
    for review in reviews:
        review.stars = range(review.rating)
    return render(request, "index.html", {'reviews': reviews})


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
        "locations": Location.objects.all(),
    }
    print(request.POST)
    if request.method == "POST":
        patients = []
        additional_test = None
        location = None
        # Parsing data from payload
        test = request.POST["test"]
        preffered_date = request.POST["date"]
        preffered_time = request.POST["preferred-time"]
        time_slot_count = Appoinment.objects.filter(preffered_date=preffered_date, preffered_time=preffered_time,payment__status=True).count()
        if time_slot_count >= 3:
            messages.error(request, "This time slot is already fully booked. Please choose another time.")
            return redirect("appoinment")  # Redirect back to the appointment page
        email = request.POST["email"]
        phone = request.POST["phone"]
        address_choice = request.POST["address-choice"]
        additional_test_id = request.POST.get("additional_tests_select")
        appoinment_type = request.POST["appointmentType"]
        amount = request.POST["amount"]

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
        patient_name = request.POST.get("full_name")
        patient_age = request.POST.get("age")
        patient_gender = request.POST.get("gender")
        patients.append(
            Patient.objects.create(
                full_name=patient_name,
                age=patient_age or None,
                gender=patient_gender or None,
            )
        )

        if appoinment_type == "Home":
            location = Location.objects.create(
                address=request.POST.get("location-address"),
                distance=request.POST.get("location-distance") or 0,
                latitude=request.POST.get("location-lat"),
                longitude=request.POST.get("location-lng"),
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
            location=location,
            amount=amount,
            user=request.user,
        )

        # Setting patients to appoinment instance
        if patients:
            _appoinment.patients.add(*patients)
        
        if request.FILES.get("prescription"):
            print(request.FILES)
            file = request.FILES["prescription"]
            _appoinment.prescription = file
        
        _appoinment.save()

        # messages.success(request, "Appoinment created successfully.")

        return redirect("payment", appoinment_id=_appoinment.object_id)

    return render(request, "appoinment.html", context)

@never_cache
@login_required
def payment(request, appoinment_id):
    appoinment = get_object_or_404(Appoinment, object_id=appoinment_id)
    if appoinment.payment_set.exists():
        messages.error(request, "Payment for this appoinment is already complete.")
        return redirect("home")
    try:
        order = generate_order(
        appoinment.amount,
        )
        appoinment.razorpay_order_id = order.get("id")
        appoinment.save()
        context = {
             "appoinment": appoinment,
             "razorpay_key_id": settings.RAZORPAY_KEY_ID,
             "order": order,
             "callback_url": request.build_absolute_uri(reverse('verify-payment')),
             }
        return render(request, "payment.html", context)
    except Exception as e:
        messages.error(request, f"Error generating order: {str(e)}")
        return redirect("appoinment", appoinment_id=appoinment_id)

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

@never_cache
@login_required(login_url='login')
def userprofile(request):
    users = User.objects.all()
    return render(request, "userprofile.html", {'users': users})
@never_cache
@login_required()
def updateprofile(request):
    users = User.objects.all()
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST["first_name"]
        user.email = request.POST["email"]
        user.phone_number = request.POST["phone"]
        user.username = request.POST["username"]
        address = user.address
        if not user.address:
            # If the address doesn't exist, you may want to create it
            address = Address()
        address.street_address = request.POST["street_address"]
        address.city = request.POST["city"]
        address.pincode = request.POST["pincode"]
        address.save()
        if request.FILES.get("profile_pic"):
            profile_pic = request.FILES["profile_pic"]
            user.profile_pic = profile_pic
        user.address = address
        user.save()
    return render(request, "updateprofile.html", {'users': users})

def get_test_price(request):
    test_id = request.GET.get('test_id')

    try:
        test = Test.objects.get(id=test_id)
        test_price = test.price  # Assuming your Test model has a "price" field
    except Test.DoesNotExist:
        test_price = None

    data = {'price': test_price}
    return JsonResponse(data)

@csrf_exempt
def verify_payment(request):
    data = request.POST
    order_id = data.get("razorpay_order_id")
    payment_id = data.get("razorpay_payment_id")
    signature = data.get("razorpay_signature")
    if not order_id:
        messages.error(request, "Invalid request.")
        return redirect("home")
    appoinment = Appoinment.objects.get(razorpay_order_id=order_id)
    Payment.objects.create(
        user=appoinment.user,
        appoinment=appoinment,
        amount=appoinment.amount,
        status=True,
        razorpay_payment_id=payment_id,
        razorpay_signature=signature,
    )
    return render(request, "payment_success.html")


@never_cache
@login_required()
def Review_rate(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        # Create a new review
        review = Review(user=request.user, comment=comment, rating=rating)
        review.save()

        messages.success(request, 'Review submitted successfully!')
        return redirect('home')  # Redirect to home or another appropriate page