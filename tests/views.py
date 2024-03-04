from decimal import Decimal
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
from datetime import datetime 
from django.db.models import Q
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from tests.models import (
    Address,
    Test,
    Patient,
    Appoinment,
    Location,
    Payment,
    Review,
    Report,
    Product,
    CartItem,
    Order,
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

        return redirect("payment", order_id=_appoinment.object_id)

    return render(request, "appoinment.html", context)

@never_cache
@login_required
def payment(request, order_id):
    order = None
    order_type = request.GET.get("order_type") or "appoinment"
    if order_type == "ecommerce":
        order = get_object_or_404(Order, pk=order_id)
        if order.payment_set.exists():
            messages.error(request, "Payment for this order is already complete.")
            return redirect("home")
    else:
        order = get_object_or_404(Appoinment, object_id=order_id)
        if order.payment_set.exists():
            messages.error(request, "Payment for this appoinment is already complete.")
            return redirect("home")
    try:
        raz_order = generate_order(
            order.total_amount if hasattr(order, "total_amount") else order.amount
        )
        order.razorpay_order_id = raz_order.get("id")
        order.save()
        context = {
            "order": order,
            "order_type": order_type,
            "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            "raz_order": raz_order,
            "callback_url": request.build_absolute_uri(reverse('verify-payment')),
        }
        return render(request, "payment.html", context)
    except Exception as e:
        messages.error(request, f"Error generating order: {str(e)}")
        if order_type == "appoinment":
            return redirect("appoinment", order_id=order_id)
        else:
            return redirect("checkout")

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

@never_cache
@csrf_exempt
def verify_payment(request):
    data = request.POST
    order_id = data.get("razorpay_order_id")
    payment_id = data.get("razorpay_payment_id")
    signature = data.get("razorpay_signature")

    if not order_id:
        messages.error(request, "Invalid request.")
        return redirect("home")

    # Retrieve the corresponding appointment based on the razorpay_order_id
    appoinment = Appoinment.objects.filter(razorpay_order_id=order_id).first()
    order = Order.objects.filter(razorpay_order_id=order_id).first()
    order_type = "ecommerce" if order else "appoinment"
    # Create Payment
    Payment.objects.create(
        user=(order or appoinment).user,
        appoinment=appoinment,
        order=order,
        amount=order.total_amount if order_type == "ecommerce" else appoinment.amount,
        status=True,
        razorpay_payment_id=payment_id,
        razorpay_signature=signature,
    )

    # Pass the appoinment details to the template context
    context = {'order': appoinment or order, "order_type": order_type}
    return render(request, "payment_success.html", context)


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
    
@never_cache
@login_required()
def myappoinment(request):
    context = {
        "tests": Test.objects.filter(is_available=True),
        "locations": Location.objects.all(),
    }

    # Fetch the user's appointments with a report
    user_appointments = Appoinment.objects.filter(user=request.user, report__isnull=False).order_by('-created_at')

    context["user_appointments"] = user_appointments

    return render(request, "myappoinment.html", context)


@never_cache
@login_required()
def payment_success(request,appoinment_id):
    appoinment = get_object_or_404(Appoinment, id=appoinment_id)

    return render(request, 'payment_successful.html', {'appoinment': appoinment})


@never_cache
def product_list(request):
    products = Product.objects.filter(Q(is_available=True, stock__gt=0) | Q(is_available=True, stock=0))
    cart_item_ids = []  
    # Logic to get cart items IDs for authenticated users
    if request.user.is_authenticated:
        cart_items = request.user.cartitem_set.all()
        cart_item_ids = [item.product.id for item in cart_items]
    context = {
        'products': products,
        'cart_item_ids': cart_item_ids,
        'user': request.user  # Assuming user authentication is handled properly
    }
    return render(request, "product.html", context)


@never_cache
@login_required()
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    return render(request, "product-detail.html", {"product": product})

@never_cache
@login_required
def add_to_cart(request):
    product_id = request.GET.get("product_id")
    quantity = request.GET.get("quantity")
    if not product_id or not quantity:
        messages.error(request, "Product ID & Quantity are mandatory.")
        return redirect("product")
    product = Product.objects.get(pk=product_id)
    quantity = int(quantity)
    # Check if the user has an existing cart item for this product
    cart_item = CartItem.objects.filter(product=product, user=request.user, order__isnull=True).first()
    if cart_item is not None:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            product=product,
            quantity=quantity,
            user=request.user,
        )
    if cart_item.quantity > product.stock:
        messages.error(request, "Cannot add more quantity than available stock.")
        return redirect("product")
    cart_item.save()
    messages.success(request, f"{product.product_name} added to cart.")
    return redirect("cart")


@never_cache
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(
        user=request.user,
        order__isnull=True,
    )
    return render(request, "cart.html", {"cart_items": cart_items})

@login_required
def update_cart_item(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart')  # Redirect to cart page after updating quantity
    return redirect('cart')  # Redirect to cart page if not a POST request


@never_cache
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(
        user=request.user,
        order__isnull=True,
    )
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.product_sale_price * item.quantity
    context = {
        "total_amount": total_amount,
        "cart_items": cart_items,
    }
    return render(request, "checkout.html", context)


@never_cache
@login_required
def order(request):
    full_name = request.POST.get("full_name")
    address = request.POST.get("address")
    city = request.POST.get("city")
    pincode = request.POST.get("pincode")
    product_id = request.POST.get("product_id", None)
    location_address=request.POST.get("location-address")
    location_distance = request.POST.get("location-distance") or 0
    location_latitude = request.POST.get("location-lat")
    location_longitude = request.POST.get("location-lng")

    
    # Retrieve the product
    product = None
    if product_id:
        product = Product.objects.get(id=product_id)
        # Check if the requested quantity is available
        if product.stock < 1:
            return HttpResponse("Product out of stock")

    # Create an address
    address = Address.objects.create(
        full_name=full_name,
        street_address=address,
        city=city,
        pincode=pincode,
    )
    
    location = Location.objects.create(
        address=location_address,
        distance=location_distance,
        latitude=location_latitude,
        longitude=location_longitude,
    )

    
    # Calculate the additional amount based on distance
    additional_amount = Decimal(location_distance) * Decimal('5')  # Assuming rate is ₹5 per kilometer
    # Perform the order creation inside a transaction
    with transaction.atomic():
        if product:
            # Create a cart item for the product
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
            )
            cart_items = [cart_item]
            # Reduce the stock of the product by the quantity ordered
            product.stock -= cart_item.quantity
            product.save()
        else:
            # Fetch cart items for the current user
            cart_items = CartItem.objects.filter(
                user=request.user,
                order__isnull=True,
            )

            # Reduce stock for each product ordered
            for item in cart_items:
                item.product.stock -= item.quantity
                item.product.save()

        # Calculate total amount
        total_amount = sum(item.total_price for item in cart_items)
        
        total_amount += additional_amount
        # Create an order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total_amount,
            location=location,
        )

        # Update cart items with the order
        cart_items.update(order=order)

    # Redirect to payment page
    return redirect(f"{reverse('payment', kwargs={'order_id': order.id})}?order_type=ecommerce")

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, pk=item_id)
        cart_item.delete()
        messages.success(request, f"{cart_item.product.product_name} removed from cart.")
    return redirect('cart')


def product_search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(
        Q(product_name__icontains=query) | 
        Q(brand__icontains=query),
        is_available=True  # Filter products with is_available=True
    ) if query else Product.objects.filter(is_available=True)
    return render(request, 'product.html', {'products': products})



def myorder(request):
    # Fetch orders for the current user along with related cart items and products
    orders = Order.objects.filter(user=request.user,  payment__status=True).prefetch_related('cartitem_set__product')

    context = {
        'orders': orders
    }
    return render(request, 'myorder.html', context)