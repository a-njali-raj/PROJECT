from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def staff_dashboard(request):
    if request.user.is_staff and not request.user.is_superuser:
        return render(request, "staff_dashboard.html")
    return redirect("home")

@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        return render(request, "admin_dashboard.html")
    return redirect("home")

