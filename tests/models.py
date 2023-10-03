from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    address = models.ForeignKey(
        "Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)


class Test(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)


class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)


class Address(models.Model):
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)


class Appoinment(models.Model):
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
