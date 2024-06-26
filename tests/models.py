import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager


class User(AbstractBaseUser):
    username = models.CharField(
        "Username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            "unique": "A user with that username already exists.",

        },
    )
    first_name = models.CharField("First name", max_length=150, blank=True)
    email = models.EmailField("Email address", blank=True)
    is_staff = models.BooleanField(
        "Staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_superuser = models.BooleanField(
        "Superuser status",
        default=False,
        help_text=(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ),
    )
    is_active = models.BooleanField(
        "Active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    last_login = None

    address = models.ForeignKey(
        "Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="media/profile-pics/", null=True, blank=True,)
    is_deliveryboy = models.BooleanField(
        "Delivery Boy Status",
        default=False,
        help_text="Designates whether the user is a delivery boy.",
    )
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    
    #admin panel settings
    def has_module_perms(self, app_label):
        return True
    def has_perm(self,perm):
        return True

class Test(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)


class Address(models.Model):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    street_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    pincode = models.CharField(max_length=6,blank=True, null=True)


class Appoinment(models.Model):
    object_id = models.UUIDField(default=uuid.uuid4, unique=True)
    main_test = models.ForeignKey(
        Test,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appoinments",
    )
    preffered_date = models.DateField()
    preffered_time = models.TimeField()
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    patients = models.ManyToManyField(Patient)
    additional_test = models.ForeignKey(
        Test,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    appoinment_type = models.CharField(max_length=10)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    prescription = models.FileField(
        upload_to="media/prescriptions/",
        null=True,
        blank=True,
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    appointment_status = models.CharField(max_length=20,default='pending')
    report = models.ForeignKey(
        "Report",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appoinment_report",
    )
class Location(models.Model):
    address = models.TextField(null=True,blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    latitude = models.CharField(max_length=50,null=True,blank=True)
    longitude = models.CharField(max_length=50,null=True,blank=True)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appoinment = models.ForeignKey(Appoinment, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    object_id = models.UUIDField(default=uuid.uuid4, unique=True)
    appoinment = models.ForeignKey(Appoinment,on_delete=models.CASCADE,related_name="report_appoinments")
    uploaded_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,)
    uploaded_at = models.DateTimeField(default=timezone.now)
    result_file = models.FileField(
        upload_to="media/results/",
        null=True,
        blank=True,
    )

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    product_image = models.ImageField(upload_to='product_images/',null=True,blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True) 

    @property
    def product_sale_price(self):
        return self.product_price - (self.product_price * (self.discount / 100))

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey("Order", null=True, blank=True, on_delete=models.CASCADE)

    @property
    def total_price(self):
        return self.product.product_price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='orders',null=True, blank=True)
    delivery_status = models.CharField(max_length=20,default='pending')
    updated_by_delivery_boy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_orders')
    