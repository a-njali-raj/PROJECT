from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import *

admin.site.register(Test)
admin.site.register(Patient)
admin.site.register(Address)
admin.site.register(Appoinment)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(Product)

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

# class MyUserAdmin(UserAdmin):
#     form = MyUserChangeForm

# admin.site.register(User, MyUserAdmin)
