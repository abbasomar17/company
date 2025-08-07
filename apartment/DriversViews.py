from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.contrib.auth.models import User
import datetime # To Parse input DateTime into Python Date Time Object

from .models import *
from .forms import AddTenantForm, EditTenantForm, AddDriverForm, EditDriverForm, AddCustomerForm, AddOwnerForm, DriverAddVehicleForm


@login_required(login_url='login')
def user_home(request):
    user = User.objects.get(id=request.user.id)
    user_obj = Drivers.objects.get(admin__user=user)
    vehicles = Vehicles.objects.filter(driver_id=user_obj)
    total_vehicle_number =vehicles.count()

    context = {
        "total_vehicle_number": total_vehicle_number,
    }
    return render(request, "user_template/user_home_template.html", context)


@login_required(login_url='login')
def user_feedback(request):
    user = User.objects.get(id=request.user.id)
    driver_obj = Drivers.objects.get(admin__user=user)
    feedback_data = FeedBackDriver.objects.filter(driver_id=driver_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'user_template/student_feedback.html', context)


@login_required(login_url='login')
def user_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('user_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        driver_obj = Drivers.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackDriver(driver_id=driver_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('user_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('user_feedback')


@login_required(login_url='login')
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    driver = Drivers.objects.get(admin__user=user)

    context={
        "user": user,
        "driver": driver
    }
    return render(request, 'user_template/student_profile.html', context)


@login_required(login_url='login')
def user_plate_number(request):
    form = DriverAddVehicleForm()
    user = User.objects.get(id=request.user.id)
    driver_obj = Drivers.objects.get(admin__user=user)
    vehicle_number = Vehicles.objects.filter(driver_id=driver_obj)

    context = {
        "vehicle_number": vehicle_number,
        "form": form,
    }
    return render(request, 'user_template/user_plate_number.html', context)


@login_required(login_url='login')
def user_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('user_profile')
    else:
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        familiar_address = request.POST.get('familiar_address')
        current_address = request.POST.get('current_address')
        working_address = request.POST.get('working_address')
        mobile_number = request.POST.get('mobile_number')

        try:
            user = User.objects.get(id=request.user.id)
            customuser = CustomUser.objects.get(user=user)
            customuser.user.first_name = first_name
            customuser.user.username = username
            customuser.user.email = email
            customuser.user.last_name = last_name
            if password != None and password != "":
                customuser.user.set_password(password)
            customuser.save()

            driver = Drivers.objects.get(admin=customuser.id)
            driver.familiar_address = familiar_address
            driver.current_address =current_address
            driver.working_address = working_address
            driver.mobile_number = mobile_number
            driver.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('user_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('user_profile')


@login_required(login_url='login')
def user_plate_number_update(request):
    if request.method == "POST":
        form = DriverAddVehicleForm(request.POST)
        if form.is_valid():
            current_address = form.cleaned_data['current_address']
            familiar_address = form.cleaned_data['familiar_address']
            working_address = form.cleaned_data['working_address']
            vehicle_type = form.cleaned_data['vehicle_type']
            pnumber = form.cleaned_data['pnumber']
            mobile_number = form.cleaned_data['mobile_number']

            user = User.objects.get(id=request.user.id)
            driver_obj = Drivers.objects.get(admin__user=user)
            vehicle_number_info = Vehicles(driver_id=driver_obj, familiar_address=familiar_address, vehicle_type=vehicle_type, pnumber=pnumber, current_address=current_address, working_address=working_address, mobile_number=mobile_number)
            vehicle_number_info.save()
            messages.success(request, "Vehicle Saved Successfully")
            return redirect('user_plate_number')


    else:
        form = DriverAddVehicleForm()
        context = {
            'form': form,
        }
        return render(request, 'user_template/user_plate_number.html', context)


@login_required(login_url='login')
def driver_view_notification(request):
    user = User.objects.get(id=request.user.id)
    driver = Drivers.objects.get(admin__user=user)
    notifications = NotificationDriver.objects.filter(driver_id=driver.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "user_template/driver_view_notification.html", context)
