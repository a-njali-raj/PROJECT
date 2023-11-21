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

class Location(models.Model):
    address = models.TextField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appoinment = models.ForeignKey(Appoinment, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
