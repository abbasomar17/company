from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
import json
from django.contrib.auth.models import User
import os
import uuid
import zipfile
import company.settings
from datetime import datetime
from zipfile import ZipFile
import string
from django.utils.crypto import get_random_string


from django.core.files.base import ContentFile

from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from .models import *
from organisation.models import *
from .forms import AddTenantForm, AddVehicleForm, EditVehicleForm, EditTenantForm, AddDriverForm, EditDriverForm, AddCustomerForm, AddOwnerForm, AlbumForm, EditApartmentForm, EmailOwnersNotificationForm, EmailTenantsNotificationForm, EmailDriversNotificationForm, EmailRandomsNotificationForm


@login_required(login_url='user_login')
def admin_home(request):
    all_driver_count = Drivers.objects.all().count()
    all_random_count = Random_users.objects.all().count()
    all_tenant_count = Tenants.objects.all().count()
    order_count = Order.objects.filter(ordered=False).count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()
    owner_count = Apartment_owners.objects.all().count()

    # Total Subjects and students in Each Course
    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    tenant_count_list_in_course = []

    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        tenants = Tenants.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        tenant_count_list_in_course.append(tenants)

    owner_all = Apartment_owners.objects.all()
    owners_name_list = []
    apartment_count_list = []
    tenant_count_list_in_owner = []

    for owner in owner_all:
        apartments = Album.objects.filter(owner_id=owner.id).count()
        tenants = Tenants.objects.filter(owner_id=owner.id).count()
        owners_name_list.append(owner.admin.user.first_name)
        apartment_count_list.append(apartments)
        tenant_count_list_in_owner.append(tenants)

    subject_all = Subjects.objects.all()
    subject_list = []
    tenant_count_list_in_subject = []
    for subject in subject_all:
        course = Courses.objects.get(id=subject.course_id.id)
        tenant_count = Tenants.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        tenant_count_list_in_subject.append(tenant_count)

    driver_name_list = []

    drivers = Drivers.objects.all()
    for driver in drivers:
        driver_name_list.append(driver.admin.user.first_name)

    driver_all = Drivers.objects.all()
    vehicle_list = []
    vehicle_count_list_in_driver = []
    for driver in driver_all:
        vehicle_count = Vehicles.objects.filter(driver_id=driver.id).count()
        vehicle_list.append(driver.admin.user.username)
        vehicle_count_list_in_driver.append(vehicle_count)

    # For Staffs
    owner_attendance_present_list = []
    owner_attendance_leave_list = []
    owner_name_list = []

    owners = Apartment_owners.objects.all()
    for owner in owners:
        subject_ids = Subjects.objects.filter(owner_id=owner.admin.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportOwner.objects.filter(owner_id=owner.id, leave_status=1).count()
        owner_attendance_present_list.append(attendance)
        owner_attendance_leave_list.append(leaves)
        owner_name_list.append(owner.admin.user.first_name)

    # For Students
    tenant_attendance_present_list = []
    tenant_attendance_leave_list = []
    tenant_name_list = []

    tenants = Tenants.objects.all()
    for tenant in tenants:
        attendance = AttendanceReport.objects.filter(tenant_id=tenant.id, status=True).count()
        absent = AttendanceReport.objects.filter(tenant_id=tenant.id, status=False).count()
        leaves = LeaveReportTenant.objects.filter(tenant_id=tenant.id, leave_status=1).count()
        tenant_attendance_present_list.append(attendance)
        tenant_attendance_leave_list.append(leaves+absent)
        tenant_name_list.append(tenant.admin.user.first_name)


    context = {
        "all_driver_count": all_driver_count,
        "all_random_count": all_random_count,
        "driver_name_list": driver_name_list,
        "order_count": order_count,
        "all_tenant_count": all_tenant_count,
        "subject_count": subject_count,
        "course_count": course_count,
        "owner_count": owner_count,
        "course_name_list": course_name_list,
        "subject_count_list": subject_count_list,
        "tenant_count_list_in_course": tenant_count_list_in_course,
        "owners_name_list": owners_name_list,
        "apartment_count_list": apartment_count_list,
        "tenant_count_list_in_owner": tenant_count_list_in_owner,
        "subject_list": subject_list,
        "tenant_count_list_in_subject": tenant_count_list_in_subject,
        "vehicle_list": vehicle_list,
        "vehicle_count_list_in_driver": vehicle_count_list_in_driver,
        "owner_attendance_present_list": owner_attendance_present_list,
        "owner_attendance_leave_list": owner_attendance_leave_list,
        "owner_name_list": owner_name_list,
        "tenant_attendance_present_list": tenant_attendance_present_list,
        "tenant_attendance_leave_list": tenant_attendance_leave_list,
        "tenant_name_list": tenant_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


@login_required(login_url='user_login')
def admin_view_ceo_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceCEOReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'hod_template/admin_ceo_attendance.html', context)


@login_required(login_url='user_login')
def admin_view_hr_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceHRReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'hod_template/admin_hr_attendance.html', context)


@login_required(login_url='user_login')
def admin_feedback(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = AdminHOD.objects.get(admin__user=user)
    feedback_data = FeedBackAdmin.objects.filter(admin_id=admin_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'hod_template/admin_feedback.html', context)


@login_required(login_url='user_login')
def admin_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('admin_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        admin_obj = AdminHOD.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackAdmin(admin_id=admin_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('admin_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('admin_feedback')


@login_required(login_url='user_login')
def cs_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = AdminHOD.objects.get(admin__user=user)
    office = admin_obj.office
    css = Customer_service.objects.filter(office=office)
    for cs in css:
        feedbacks = FeedBackCS.objects.filter(cs_id=cs)
        context = {
            "feedbacks": feedbacks
        }
        return render(request, 'hod_template/cs_feedback_template.html', context)


@csrf_exempt
def cs_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackCS.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def my_view_admin_resp(request):
    obj = User.objects.get(id=request.user.id)
    user_obj = AdminHOD.objects.get(admin__user=obj)
    office = user_obj.office
    resps = ResponsibilityAdmin.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'hod_template/view_admin_resp.html', context)


@login_required(login_url='user_login')
def admin_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = AdminHOD.objects.get(admin__user=user)
    leave_data = LeaveReportAdmin.objects.filter(admin_id=admin_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'hod_template/admin_apply_leave.html', context)


@login_required(login_url='user_login')
def admin_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('admin_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        admin_obj = AdminHOD.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportAdmin(admin_id=admin_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('admin_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('admin_apply_leave')


@login_required(login_url='user_login')
def admin_apply_permission(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = AdminHOD.get(admin__user=user)
    permission_data = PermissionReportAdmin.objects.filter(admin_id=admin_obj)
    context = {
        "permission_data": permission_data
    }
    return render(request, 'hod_template/admin_apply_permission.html', context)


@login_required(login_url='user_login')
def admin_view_notification(request):
    user = User.objects.get(id=request.user.id)
    admin = AdminHOD.objects.get(admin__user=user)
    notifications = NotificationAdmin.objects.filter(admin_id=admin.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "hod_template/admin_view_notification.html", context)


@login_required(login_url='user_login')
def admin_view_def_notification(request):
    user = User.objects.get(id=request.user.id)
    admin = AdminHOD.objects.get(user=user)
    def_notifications = DefendantNotificationAdmin.objects.filter(admin_id=admin.id)
    context = {
        "notifications": def_notifications,
    }
    return render(request, "hod_template/admin_view_def_notification.html", context)


@login_required(login_url='user_login')
def admin_view_acu_notification(request):
    user = User.objects.get(id=request.user.id)
    admin = AdminHOD.objects.get(user=user)
    acu_notifications = AccusserNotificationAdmin.objects.filter(admin_id=admin.id)
    context = {
        "notifications": acu_notifications,
    }
    return render(request, "hod_template/admin_view_acu_notification.html", context)


@login_required(login_url='user_login')
def admin_apply_permission_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('admin_permission_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        admin_obj = AdminHOD.objects.get(admin__user=user)
        try:
            leave_report = PermissionReportAdmin(admin_id=admin_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('admin_apply_permission')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('admin_apply_permission')


@login_required(login_url='user_login')
def change_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    ap_order = OrderApartment.objects.get(order=order)
    if order.ordered == False:
        try:
            order.ordered = True
            ap_order.ordered = True
            order.save()
            ap_order.save()
            messages.success(request, "Booking Status Changed Successfully ")
            return redirect('new_orders')
        except:
            messages.error(request, "Failed to Change Booking Status.")
            return redirect('new_orders')
    else:
        messages.error(request, "Booking Status was Already changed ")
        return redirect('new_orders')


class ManageOrderView(View):
    def get(self, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                orders = Order.objects.get(ordered=True)
                context = {
                    'orders': orders
                }
                return render(self.request, "hod_template/manage_order_template.html", context)
            except ObjectDoesNotExist:
                return redirect('admin_home')
        else:
            return redirect('login')


@login_required(login_url='user_login')
def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    try:
        order.delete()
        messages.success(request, "Booking Deleted Successfully.")
        return redirect('manage_order')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_order')


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                orders = Order.objects.get(ordered=False)
                context = {
                    'orders': orders
                }
                return render(self.request, "hod_template/order_summary.html", context)
            except ObjectDoesNotExist:
                return redirect('admin_home')
        else:
            return redirect('login')


class OrdersView(View):
    """View for orders page."""

    def get(self, request):
        if request.user.is_authenticated:
            p = Paginator(Order.objects.filter(ordered=False), 25)
            page = request.GET.get('page')
            orders = p.get_page(page)
            context = {
                'orders': orders,
            }
            if 'search_query' in request.GET:
                query = request.GET.get('search_query')
                if query == '':
                    p = Paginator(
                        Order.objects.filter(ordered=False),
                        25
                    )
                    page = request.GET.get('page')
                    orders = p.get_page(page)
                    context = {
                        'orders': orders,
                    }
                    return render(
                        request,
                        'hod_template/orders.html',
                        context
                    )
                orders = Order.objects.filter(
                      Q(phone__icontains=query) |
                      Q(ordered_date__icontains=query) |
                      Q(ref_code__icontains=query)
                )
                p = Paginator(orders, 25)
                page = request.GET.get('page')
                orders = p.get_page(page)
                context = {
                    'orders': orders,
                }
                return render(
                    request,
                    'hod_template/orders.html',
                    context
                )
            return render(request, 'hod_template/orders.html', context)
        else:
            return redirect('login')


class ManageOrdersView(View):
    """View for orders page."""

    def get(self, request):
        """Get method for orders page."""
        if request.user.is_authenticated:
            p = Paginator(Order.objects.filter(ordered=True), 25)
            page = request.GET.get('page')
            orders = p.get_page(page)
            context = {
                'orders': orders,
            }
            if 'search_query' in request.GET:
                query = request.GET.get('search_query')
                if query == '':
                    p = Paginator(
                        Order.objects.filter(ordered=True),
                        25
                    )
                    page = request.GET.get('page')
                    orders = p.get_page(page)
                    context = {
                        'orders': orders,
                    }
                    return render(
                        request,
                        'hod_template/manage_order_template.html',
                        context
                    )
                orders = Order.objects.filter(
                      Q(phone__icontains=query) |
                      Q(ordered_date__icontains=query) |
                      Q(ref_code__icontains=query)
                )
                p = Paginator(orders, 25)
                page = request.GET.get('page')
                orders = p.get_page(page)
                context = {
                    'orders': orders,
                }
                return render(
                    request,
                    'hod_template/manage_order_template.html',
                    context
                )
            return render(request, 'hod_template/manage_order_template.html', context)
        else:
            return redirect('login')


class OrderDetailsView(View):
    """View for order full page."""

    def get(self, request, *args, **kwargs):
        """Get method for order details page."""
        if request.user.is_authenticated:
            order_id = kwargs['order_id']
            order = get_object_or_404(Order, id=order_id)
            order_items = OrderApartment.objects.filter(order=order)
            context = {
                'order': order,
                'order_items': order_items,

            }
            return render(request, 'hod_template/order_details.html', context)
        else:
            return redirect('admin_home')


@login_required(login_url='user_login')
def manage_random(request):
    randoms = Random_users.objects.all()
    context = {
        "randoms": randoms
    }
    return render(request, "hod_template/manage_random_template.html", context)


@login_required(login_url='user_login')
def edit_random(request, random_id):
    request.session['random_id'] = random_id
    rendom = Random_users.objects.get(id=random_id)

    context = {
        "rendom": rendom,
        "id": random_id
    }
    return render(request, "hod_template/edit_random_template.html", context)


@login_required(login_url='user_login')
def edit_random_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        random_id = request.session.get('random_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        last_name = request.POST.get('last_name')

        try:
            # INSERTING into Customuser Model
            user = Random_users.objects.get(id=random_id)
            user.admin.user.first_name = first_name
            user.admin.user.last_name = last_name
            user.admin.user.email = email
            user.admin.user.username = username
            user.admin.user.password = password
            user.save()

            messages.success(request, "Owner Updated Successfully.")
            return redirect('/edit_random/' + random_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_random/' + random_id)


@login_required(login_url='user_login')
def delete_random(request, random_id):
    rendom = Random_users.objects.get(id=random_id)
    try:
        rendom.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_random')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_random')


@login_required(login_url='user_login')
def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


@login_required(login_url='user_login')
def add_staff_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        owner_form = AddOwnerForm(request.POST)
        if customer_form.is_valid() and owner_form.is_valid():
            user = User(email=request.POST['email'], username=request.POST['username'], password=request.POST['password'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
            user.save()
            customer = CustomUser(user_type=2, user=user)
            customer.save()
            owner = owner_form.save(commit=False)
            owner.admin = customer
            owner.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
    else:
        customer_form = AddCustomerForm()
        owner_form = AddOwnerForm()
        context = {
            'customer_form': customer_form,
            'owner_form': owner_form
        }
        return render(request,'hod_template/add_staff_template.html', context)


@login_required(login_url='user_login')
def manage_staff(request):
    owners = Apartment_owners.objects.all()
    context = {
        "owners": owners
    }
    return render(request, "hod_template/manage_staff_template.html", context)


@login_required(login_url='user_login')
def edit_staff(request, owner_id):
    request.session['owner_id'] = owner_id
    owner = Apartment_owners.objects.get(id=owner_id)

    context = {
        "owner": owner,
        "id": owner_id
    }
    return render(request, "hod_template/edit_staff_template.html", context)


@login_required(login_url='user_login')
def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        owner_id = request.session.get('owner_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            # INSERTING into Customuser Model
            user_obj = Apartment_owners.objects.get(id=owner_id)

            user_obj.admin.user.first_name = first_name
            user_obj.admin.user.last_name = last_name
            user_obj.admin.user.email = email
            user_obj.admin.user.username = username
            user_obj.admin.user.password = password
            user_obj.address = address
            user_obj.save()


            messages.success(request, "Owner Updated Successfully.")
            return redirect('/edit_staff/'+owner_id)

        except:
            messages.error(request, "Failed to Update Staff.")
            return redirect('/edit_staff/'+owner_id)


@login_required(login_url='user_login')
def delete_staff(request, owner_id):
    owner = Apartment_owners.objects.get(id=owner_id)
    try:
        owner.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_staff')


@login_required(login_url='user_login')
def add_user(request):
    form = AddDriverForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_user_template.html', context)


@login_required(login_url='user_login')
def add_user_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        driver_form = AddDriverForm(request.POST, request.FILES)
        if customer_form.is_valid() and driver_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            current_address = driver_form.cleaned_data['current_address']
            region = driver_form.cleaned_data['region']
            familiar_address = driver_form.cleaned_data['familiar_address']
            working_address = driver_form.cleaned_data['working_address']
            gender = driver_form.cleaned_data['gender']
            vehicle_type = driver_form.cleaned_data['vehicle_type']
            nida_number = driver_form.cleaned_data['nida_number']
            tin_number = driver_form.cleaned_data['tin_number']
            lnumber = driver_form.cleaned_data['lnumber']
            pnumber = driver_form.cleaned_data['pnumber']
            mobile_number = driver_form.cleaned_data['mobile_number']
            if len(request.FILES) != 0:
                profile_picture = request.FILES['profile_picture']
                fs = FileSystemStorage()
                filename = fs.save(profile_picture.name, profile_picture)
                profile_picture_url = fs.url(filename)
            else:
                profile_picture_url = None
            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = CustomUser(user_type = 4, user=user)
            customer.save()
            driver = Drivers(admin=customer, current_address=current_address, region=region, familiar_address=familiar_address, working_address=working_address, gender=gender, vehicle_type=vehicle_type, nida_number=nida_number, tin_number=tin_number, lnumber=lnumber, pnumber=pnumber, mobile_number=mobile_number, profile_picture=profile_picture_url)
            driver.save()
            messages.success(request, "User Added Successfully!")
            return redirect('add_user')
    else:
        customer_form = AddCustomerForm()
        driver_form = AddDriverForm()
        context = {
            'customer_form': customer_form,
            'driver_form': driver_form
        }
        return render(request,'hod_template/add_user_template.html', context)


@login_required(login_url='user_login')
def manage_user(request):
    drivers = Drivers.objects.all()
    context = {
        "drivers": drivers
    }
    return render(request, 'hod_template/manage_user_template.html', context)


@login_required(login_url='user_login')
def edit_user(request, driver_id):
    # Adding Student ID into Session Variable
    request.session['driver_id'] = driver_id

    driver = Drivers.objects.get(id=driver_id)
    form = EditDriverForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = driver.admin.user.email
    form.fields['username'].initial = driver.admin.user.username
    form.fields['first_name'].initial = driver.admin.user.first_name
    form.fields['last_name'].initial = driver.admin.user.last_name
    form.fields['current_address'].initial = driver.current_address
    form.fields['familiar_address'].initial = driver.familiar_address
    form.fields['working_address'].initial = driver.working_address
    form.fields['gender'].initial = driver.gender
    form.fields['vehicle_type'].initial = driver.vehicle_type

    context = {
        "id": driver_id,
        "username": driver.admin.user.username,
        "form": form
    }
    return render(request, "hod_template/edit_user_template.html", context)


@login_required(login_url='user_login')
def edit_user_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        driver_id = request.session.get('driver_id')
        if driver_id == None:
            return redirect('/manage_user')

        form = EditDriverForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            current_address = form.cleaned_data['current_address']
            familiar_address = form.cleaned_data['familiar_address']
            working_address = form.cleaned_data['working_address']
            gender = form.cleaned_data['gender']
            vehicle_type = form.cleaned_data['vehicle_type']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_picture = request.FILES['profile_picture']
                fs = FileSystemStorage()
                filename = fs.save(profile_picture.name, profile_picture)
                profile_picture_url = fs.url(filename)
            else:
                profile_picture_url = None

            try:
                # First Update into Custom User Model
                user = Drivers.objects.get(id=driver_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username


                # Then Update Students Table

                user.current_address = current_address
                user.familiar_address = familiar_address
                user.working_address = working_address

                user.gender = gender
                user.vehicle_type = vehicle_type
                if profile_picture_url != None:
                    user.profile_picture = profile_picture_url
                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['driver_id']

                messages.success(request, "User Updated Successfully!")
                return redirect('/edit_user/'+driver_id)
            except:
                messages.success(request, "Failed to Update User.")
                return redirect('/edit_user/'+driver_id)
        else:
            return redirect('/edit_user/'+driver_id)


@login_required(login_url='user_login')
def delete_user(request, driver_id):
    driver = Drivers.objects.get(id=driver_id)
    try:
        driver.delete()
        messages.success(request, "User Deleted Successfully.")
        return redirect('manage_user')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_user')


@login_required(login_url='user_login')
def add_course(request):
    return render(request, "hod_template/add_course_template.html")


@login_required(login_url='user_login')
def add_course_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_course')
    else:
        course = request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Course Added Successfully!")
            return redirect('add_course')
        except:
            messages.error(request, "Failed to Add Course!")
            return redirect('add_course')


@login_required(login_url='user_login')
def manage_course(request):
    courses = Courses.objects.all()
    context = {
        "courses": courses
    }
    return render(request, 'hod_template/manage_course_template.html', context)


@login_required(login_url='user_login')
def edit_course(request, course_id):
    request.session['course_id'] = course_id
    course = Courses.objects.get(id=course_id)
    context = {
        "course": course,
        "id": course_id
    }
    return render(request, 'hod_template/edit_course_template.html', context)


@login_required(login_url='user_login')
def edit_course_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        course_id = request.session.get('course_id')
        course_name = request.POST.get('course')

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_course/'+course_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_course/'+course_id)


@login_required(login_url='user_login')
def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
        return redirect('manage_course')
    except:
        messages.error(request, "Failed to Delete Course.")
        return redirect('manage_course')


@login_required(login_url='user_login')
def manage_session(request):
    session_years = SessionYearModel.objects.all()
    context = {
        "session_years": session_years
    }
    return render(request, "hod_template/manage_session_template.html", context)


@login_required(login_url='user_login')
def add_session(request):
    return render(request, "hod_template/add_session_template.html")


@login_required(login_url='user_login')
def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_session')
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("add_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("add_session")


@login_required(login_url='user_login')
def edit_session(request, session_id):
    request.session['session_id'] = session_id
    session_year = SessionYearModel.objects.get(id=session_id)
    context = {
        "session_year": session_year
    }
    return render(request, "hod_template/edit_session_template.html", context)


@login_required(login_url='user_login')
def edit_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_session')
    else:
        session_id = request.session.get('session_id')
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        try:
            session_year = SessionYearModel.objects.get(id=session_id)
            session_year.session_start_year = session_start_year
            session_year.session_end_year = session_end_year
            session_year.save()

            messages.success(request, "Session Year Updated Successfully.")
            return redirect('/edit_session/'+session_id)
        except:
            messages.error(request, "Failed to Update Session Year.")
            return redirect('/edit_session/'+session_id)


@login_required(login_url='user_login')
def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully.")
        return redirect('manage_session')
    except:
        messages.error(request, "Failed to Delete Session.")
        return redirect('manage_session')


@login_required(login_url='user_login')
def add_student(request):
    form = AddTenantForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_student_template.html', context)


@login_required(login_url='user_login')
def add_student_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        tenant_form = AddTenantForm(request.POST, request.FILES)
        if customer_form.is_valid() and tenant_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = tenant_form.cleaned_data['address']
            nida_number = tenant_form.cleaned_data['nida_number']
            session_year_id = tenant_form.cleaned_data['session_year_id']
            course_id = tenant_form.cleaned_data['course_id']
            apartment_id = tenant_form.cleaned_data['apartment_id']
            owner_id = tenant_form.cleaned_data['owner_id']
            gender = tenant_form.cleaned_data['gender']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = CustomUser(user=user, user_type = 3)
            customer.save()
            course_obj = Courses.objects.get(id=course_id)

            apartment_obj = Album.objects.get(id=apartment_id)

            owner_obj = Apartment_owners.objects.get(id=owner_id)

            session_year_obj = SessionYearModel.objects.get(id=session_year_id)

            tenant = Tenants(admin=customer, owner_id=owner_obj, apartment_id=apartment_obj, address=address, nida_number=nida_number, gender=gender, course_id=course_obj, session_year_id=session_year_obj, profile_pic=profile_pic_url)
            tenant.save()
            messages.success(request, "Tenant Added Successfully!")
            return redirect('add_student')
    else:
        customer_form = AddCustomerForm()
        tenant_form = AddTenantForm()
        context = {
            'customer_form': customer_form,
            'tenant_form': tenant_form
        }
        return render(request, 'hod_template/add_student_template.html', context)


@login_required(login_url='user_login')
def manage_student(request):
    tenants = Tenants.objects.all()
    context = {
        "tenants": tenants
    }
    return render(request, 'hod_template/manage_student_template.html', context)


@login_required(login_url='user_login')
def edit_student(request, tenant_id):
    # Adding Student ID into Session Variable
    request.session['tenant_id'] = tenant_id

    tenant = Tenants.objects.get(admin=tenant_id)
    form = EditTenantForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = tenant.admin.user.email
    form.fields['username'].initial = tenant.admin.user.username
    form.fields['first_name'].initial = tenant.admin.user.first_name
    form.fields['last_name'].initial = tenant.admin.user.last_name
    form.fields['address'].initial = tenant.address
    form.fields['nida_number'].initial = tenant.nida_number
    form.fields['course_id'].initial = tenant.course_id.id
    form.fields['gender'].initial = tenant.gender
    form.fields['session_year_id'].initial = tenant.session_year_id.id

    context = {
        "id": tenant_id,
        "username": tenant.admin.user.username,
        "form": form
    }
    return render(request, "hod_template/edit_student_template.html", context)


@login_required(login_url='user_login')
def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        tenant_id = request.session.get('tenant_id')
        if tenant_id == None:
            return redirect('/manage_student')

        form = EditTenantForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            nida_number = form.cleaned_data['nida_number']
            course_id = form.cleaned_data['course_id']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = Tenants.objects.get(id=tenant_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username


                # Then Update Students Table

                user.address = address

                course = Courses.objects.get(id=course_id)
                user.course_id = course

                session_year_obj = SessionYearModel.objects.get(id=session_year_id)
                user.session_year_id = session_year_obj

                user.nida_number = nida_number
                user.gender = gender
                if profile_pic_url != None:
                    user.profile_pic = profile_pic_url
                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['student_id']

                messages.success(request, "Student Updated Successfully!")
                return redirect('/edit_student/'+tenant_id)
            except:
                messages.success(request, "Failed to Uupdate Student.")
                return redirect('/edit_student/'+tenant_id)
        else:
            return redirect('/edit_student/'+tenant_id)


@login_required(login_url='user_login')
def delete_student(request, tenant_id):
    tenant = Tenants.objects.get(id=tenant_id)
    try:
        tenant.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


@login_required(login_url='user_login')
def add_vehicle(request):
    form = AddVehicleForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_vehicle_template.html', context)


@login_required(login_url='user_login')
def add_vehicle_save(request):
    if request.method == "POST":
        form = AddVehicleForm(request.POST)
        if form.is_valid():
            pnumber = form.cleaned_data['pnumber']
            current_address = form.cleaned_data['current_address']
            familiar_address = form.cleaned_data['familiar_address']
            working_address = form.cleaned_data['working_address']
            mobile_number = form.cleaned_data['mobile_number']
            driver_id = form.cleaned_data['driver_id']
            vehicle_type = form.cleaned_data['vehicle_type']

            driver_obj = Drivers.objects.get(id=driver_id)

            vehicle = Vehicles(pnumber=pnumber, mobile_number=mobile_number, driver_id=driver_obj, current_address=current_address, familiar_address=familiar_address,
                              working_address=working_address, vehicle_type=vehicle_type)
            vehicle.save()
            messages.success(request, "Vehicle Added Successfully!")
            return redirect('add_vehicle')
    else:
        form = AddVehicleForm()
        context = {
            'form': form
        }
        return render(request, 'hod_template/add_vehicle_template.html', context)


@login_required(login_url='user_login')
def manage_vehicle(request):
    vehicles = Vehicles.objects.all()
    context = {
        "vehicles": vehicles
    }
    return render(request, 'hod_template/manage_vehicle_template.html', context)


@login_required(login_url='user_login')
def edit_vehicle(request, vehicle_id):
    # Adding Student ID into Session Variable
    request.session['vehicle_id'] = vehicle_id

    vehicle = Vehicles.objects.get(id=vehicle_id)
    form = EditVehicleForm()
    # Filling the form with Data from Database
    form.fields['pnumber'].initial = vehicle.pnumber
    form.fields['mobile_number'].initial = vehicle.mobile_number
    form.fields['current_address'].initial = vehicle.current_address
    form.fields['working_address'].initial = vehicle.working_address
    form.fields['familiar_address'].initial = vehicle.familiar_address
    form.fields['vehicle_type'].initial = vehicle.vehicle_type
    form.fields['driver_id'].initial = vehicle.driver_id.id

    context = {
        "id": vehicle_id,
        "pnumber": vehicle.pnumber,
        "form": form
    }
    return render(request, "hod_template/edit_vehicle_template.html", context)


@login_required(login_url='user_login')
def edit_vehicle_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        vehicle_id = request.session.get('vehicle_id')
        if vehicle_id == None:
            return redirect('/manage_vehicle')

        form = EditVehicleForm(request.POST)
        if form.is_valid():
            pnumber = form.cleaned_data['pnumber']
            mobile_number = form.cleaned_data['mobile_number']
            current_address = form.cleaned_data['current_address']
            familiar_address = form.cleaned_data['familiar_address']
            working_address = form.cleaned_data['working_address']
            vehicle_type = form.cleaned_data['vehicle_type']
            driver_id = form.cleaned_data['driver_id']


            try:

                # Then Update Students Table
                vehicle_model = Vehicles.objects.get(id=vehicle_id)
                vehicle_model.pnumber = pnumber
                vehicle_model.mobile_number = mobile_number
                vehicle_model.current_address = current_address
                vehicle_model.familiar_address = familiar_address
                vehicle_model.working_address = working_address
                vehicle_model.vehicle_type = vehicle_type


                driver_obj = Drivers.objects.get(id=driver_id)
                vehicle_model.driver_id = driver_obj

                vehicle_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['vehicle_id']

                messages.success(request, "Vehicle Updated Successfully!")
                return redirect('/edit_vehicle/'+vehicle_id)
            except:
                messages.success(request, "Failed to Update Vehicle.")
                return redirect('/edit_vehicle/'+vehicle_id)
        else:
            return redirect('/edit_vehicle/'+vehicle_id)


@login_required(login_url='user_login')
def delete_vehicle(request, vehicle_id):
    vehicle = Vehicles.objects.get(id=vehicle_id)
    try:
        vehicle.delete()
        messages.success(request, "Vehicle Deleted Successfully.")
        return redirect('manage_vehicle')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_vehicle')


@login_required(login_url='user_login')
def add_apartment(request):
    form = AlbumForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_apartment_template.html', context)


@login_required(login_url='user_login')
def add_apartment_save(request):
    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            spec_location = form.cleaned_data['spec_location']
            region = form.cleaned_data['region']
            town = form.cleaned_data['town']
            price = form.cleaned_data['price']
            discount_price = form.cleaned_data['discount_price']
            quantity = form.cleaned_data['quantity']
            booking_id = form.cleaned_data['booking_id']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            session_year_id = form.cleaned_data['session_year_id']
            owner_id = form.cleaned_data['owner_id']
            labels = form.cleaned_data['labels']

            if len(request.FILES) != 0:
                thumb = request.FILES['thumb']
                fs = FileSystemStorage()
                filename = fs.save(thumb.name, thumb)
                thumb_url = fs.url(filename)
            else:
                thumb_url = None

            session_year_obj = SessionYearModel.objects.get(id=session_year_id)
            owner_obj = Apartment_owners.objects.get(id=owner_id)

            slug = get_random_string(length=8)

            album = Album(title=title, spec_location=spec_location, region=region, town=town, price=price,
                          discount_price=discount_price, quantity=quantity, category=category, labels=labels, booking_id=booking_id,
                          description=description, session_year_id=session_year_obj, thumb=thumb_url, owner_id=owner_obj, slug = slug, modified = datetime.now(), is_visible=True)
            album.save()
            if form.cleaned_data['zip'] != None:
                zip = zipfile.ZipFile(form.cleaned_data['zip'])
                for filename in sorted(zip.namelist()):

                    file_name = os.path.basename(filename)
                    if not file_name:
                        continue

                    data = zip.read(filename)
                    contentfile = ContentFile(data)

                    img = AlbumImage()
                    img.album = album
                    img.alt = filename
                    filename = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
                    img.image.save(filename, contentfile)

                    img.thumb.save('thumb-{0}'.format(filename), contentfile)
                    img.save()
                zip.close()
            messages.success(request, "Apartment Added Successfully!")
            return redirect('add_apartment')
    else:
        form = AlbumForm()
        context = {
            'form': form
        }
        return render(request, 'hod_template/add_apartment_template.html', context)


@login_required(login_url='user_login')
def manage_apartment(request):
    albums = Album.objects.all()
    context = {
        "albums": albums
    }
    return render(request, 'hod_template/manage_apartment_template.html', context)


@login_required(login_url='user_login')
def edit_apartment(request, apartment_id):
    # Adding Student ID into Session Variable
    request.session['apartment_id'] = apartment_id

    apartment = Album.objects.get(id=apartment_id)
    form = EditApartmentForm()
    # Filling the form with Data from Database
    form.fields['title'].initial = apartment.title
    form.fields['spec_location'].initial = apartment.spec_location
    form.fields['region'].initial = apartment.region
    form.fields['town'].initial = apartment.town
    form.fields['price'].initial = apartment.price
    form.fields['quantity'].initial = apartment.quantity
    form.fields['discount_price'].initial = apartment.discount_price
    form.fields['booking_id'].initial = apartment.booking_id
    form.fields['description'].initial = apartment.description
    form.fields['category'].initial = apartment.category
    form.fields['labels'].initial = apartment.labels
    form.fields['session_year_id'].initial = apartment.session_year_id.id
    form.fields['owner_id'].initial = apartment.owner_id.id

    context = {
        "id": apartment_id,
        "username": apartment.owner_id.admin.user.username,
        "form": form
    }
    return render(request, "hod_template/edit_apartment_template.html", context)


@login_required(login_url='user_login')
def edit_apartment_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        apartment_id = request.session.get('apartment_id')
        if apartment_id == None:
            return redirect('/manage_apartment')

        form = EditApartmentForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            spec_location = form.cleaned_data['spec_location']
            region = form.cleaned_data['region']
            town = form.cleaned_data['town']
            price = form.cleaned_data['price']
            discount_price = form.cleaned_data['discount_price']
            quantity = form.cleaned_data['quantity']
            booking_id = form.cleaned_data['booking_id']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            labels = form.cleaned_data['labels']
            session_year_id = form.cleaned_data['session_year_id']
            owner_id = form.cleaned_data['owner_id']

            session_year_obj = SessionYearModel.objects.get(id=session_year_id)
            owner_obj = Apartment_owners.objects.get(id=owner_id)


            if len(request.FILES) != 0:
                thumb = request.FILES['thumb']
                fs = FileSystemStorage()
                filename = fs.save(thumb.name, thumb)
                thumb_url = fs.url(filename)
            else:
                thumb_url = None

            try:
                # First Update into Custom User Model

                # Then Update Students Table
                apartment_model = Album.objects.get(id=apartment_id)
                apartment_model.title = title
                apartment_model.spec_location = spec_location
                apartment_model.region = region
                apartment_model.town = town
                apartment_model.price = price
                apartment_model.discount_price = discount_price
                apartment_model.quantity = quantity
                apartment_model.booking_id = booking_id
                apartment_model.description = description
                apartment_model.session_year_id = session_year_obj
                apartment_model.owner_id = owner_obj
                apartment_model.category = category
                apartment_model.labels = labels
                if thumb_url != None:
                    apartment_model.thumb = thumb_url
                apartment_model.save()
                # Delete student_id SESSION after the data is updated
                del request.session['apartment_id']

                messages.success(request, "Apartment Updated Successfully!")
                return redirect('/edit_apartment/' + apartment_id)
            except:
                messages.success(request, "Failed to Update User.")
                return redirect('/edit_apartment/' + apartment_id)
        else:
            return redirect('/edit_apartment/' + apartment_id)


@login_required(login_url='user_login')
def delete_apartment(request, apartment_id):
    album = Album.objects.get(id=apartment_id)
    pictures = AlbumImage.objects.filter(album=album)
    try:
        for picture in pictures:
            picture.delete()
        album.delete()
        messages.success(request, "Apartment Deleted Successfully.")
        return redirect('manage_apartment')
    except:
        messages.error(request, "Failed to Delete Apartment.")
        return redirect('manage_apartment')


@login_required(login_url='user_login')
def user_feedback_message(request):
    feedbacks = FeedBackDriver.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/user_feedback_template.html', context)


@csrf_exempt
def user_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackDriver.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def add_subject(request):
    courses = Courses.objects.all()
    owners = CustomUser.objects.filter(user_type='2')
    context = {
        "courses": courses,
        "owners": owners
    }
    return render(request, 'hod_template/add_subject_template.html', context)


@login_required(login_url='user_login')
def add_subject_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_subject')
    else:
        subject_name = request.POST.get('subject')

        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)

        owner_id = request.POST.get('owner')
        owner = CustomUser.objects.get(id=owner_id)

        try:
            subject = Subjects(subject_name=subject_name, course_id=course, owner_id=owner)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('add_subject')
        except:
            messages.error(request, "Failed to Add Subject!")
            return redirect('add_subject')


@login_required(login_url='user_login')
def manage_subject(request):
    subjects = Subjects.objects.all()
    context = {
        "subjects": subjects
    }
    return render(request, 'hod_template/manage_subject_template.html', context)


@login_required(login_url='user_login')
def edit_subject(request, subject_id):
    request.session['subject_id'] = subject_id
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    owners = CustomUser.objects.filter(user_type='2')
    context = {
        "subject": subject,
        "courses": courses,
        "owners": owners,
        "id": subject_id
    }
    return render(request, 'hod_template/edit_subject_template.html', context)


@login_required(login_url='user_login')
def edit_subject_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        subject_id = request.session.get('subject_id')
        subject_name = request.POST.get('subject')
        course_id = request.POST.get('course')
        owner_id = request.POST.get('owner')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name

            course = Courses.objects.get(id=course_id)
            subject.course_id = course

            owner = CustomUser.objects.get(id=owner_id)
            subject.owner_id = owner
            
            subject.save()

            messages.success(request, "Subject Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))

        except:
            messages.error(request, "Failed to Update Subject.")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id":subject_id}))
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return redirect('manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return redirect('manage_subject')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@login_required(login_url='user_login')
def student_feedback_message(request):
    feedbacks = FeedBackTenant.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/student_feedback_template.html', context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackTenant.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def staff_feedback_message(request):
    feedbacks = FeedBackOwner.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackOwner.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def student_leave_view(request):
    leaves = LeaveReportTenant.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)


@login_required(login_url='login')
def student_leave_approve(request, leave_id):
    leave = LeaveReportTenant.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


@login_required(login_url='user_login')
def student_leave_reject(request, leave_id):
    leave = LeaveReportTenant.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')


@login_required(login_url='user_login')
def staff_leave_view(request):
    leaves = LeaveReportOwner.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)


@login_required(login_url='user_login')
def staff_leave_approve(request, leave_id):
    leave = LeaveReportOwner.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


@login_required(login_url='user_login')
def staff_leave_reject(request, leave_id):
    leave = LeaveReportOwner.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


@login_required(login_url='user_login')
def add_owners_email(request):
    form = EmailOwnersNotificationForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_owners_email_template.html', context)


@login_required(login_url='user_login')
def add_owners_email_save(request):
    if request.method == "POST":
        form = EmailOwnersNotificationForm(request.POST)
        if form.is_valid():
            email_name = form.cleaned_data['email_name']
            content = form.cleaned_data['content']
            code = form.cleaned_data['code']

            email = EmailOwnersNotification(email_name=email_name, content=content, code=code)
            email.save()
            messages.success(request, "Email Sent Successfully!")
            return redirect('add_owners_email')
    else:
        form = EmailOwnersNotificationForm()
        context = {
            'form': form
        }
        return render(request, 'hod_template/add_owners_email_template.html', context)


@login_required(login_url='user_login')
def manage_owners_email(request):
    emails = EmailOwnersNotification.objects.all()
    context = {
        "emails": emails
    }
    return render(request, 'hod_template/manage_owners_email_template.html', context)


@login_required(login_url='user_login')
def add_tenants_email(request):
    form = EmailTenantsNotificationForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_tenants_email_template.html', context)


@login_required(login_url='user_login')
def add_tenants_email_save(request):
    if request.method == "POST":
        form = EmailTenantsNotificationForm(request.POST)
        if form.is_valid():
            email_name = form.cleaned_data['email_name']
            content = form.cleaned_data['content']
            code = form.cleaned_data['code']

            email = EmailTenantsNotification(email_name=email_name, content=content, code=code)
            email.save()
            messages.success(request, "Email Sent Successfully!")
            return redirect('add_tenants_email')
    else:
        form = EmailTenantsNotificationForm()
        context = {
            'form': form
        }
        return render(request, 'hod_template/add_tenants_email_template.html', context)


@login_required(login_url='user_login')
def manage_tenants_email(request):
    emails = EmailTenantsNotification.objects.all()
    context = {
        "emails": emails
    }
    return render(request, 'hod_template/manage_tenants_email_template.html', context)


@login_required(login_url='user_login')
def add_drivers_email(request):
    form = EmailDriversNotificationForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_drivers_email_template.html', context)


@login_required(login_url='user_login')
def add_drivers_email_save(request):
    if request.method == "POST":
        form = EmailDriversNotificationForm(request.POST)
        if form.is_valid():
            email_name = form.cleaned_data['email_name']
            content = form.cleaned_data['content']
            code = form.cleaned_data['code']

            email = EmailDriversNotification(email_name=email_name, content=content, code=code)
            email.save()
            messages.success(request, "Email Sent Successfully!")
            return redirect('add_drivers_email')
    else:
        form = EmailDriversNotificationForm()
        context = {
            'form': form
        }
        return render(request, 'hod_template/add_drivers_email_template.html', context)


@login_required(login_url='user_login')
def manage_drivers_email(request):
    emails = EmailDriversNotification.objects.all()
    context = {
        "emails": emails
    }
    return render(request, 'hod_template/manage_drivers_email_template.html', context)


@login_required(login_url='user_login')
def add_randoms_email(request):
    form = EmailRandomsNotificationForm()
    context = {
        "form": form
    }
    return render(request, 'hod_template/add_randoms_email_template.html', context)


@login_required(login_url='user_login')
def add_randoms_email_save(request):
    if request.method == "POST":
        form = EmailRandomsNotificationForm(request.POST)
        if form.is_valid():
            email_name = form.cleaned_data['email_name']
            content = form.cleaned_data['content']
            code = form.cleaned_data['code']

            email = EmailRandomsNotification(email_name=email_name, content=content, code=code)
            email.save()
            messages.success(request, "Email Sent Successfully!")
            return redirect('add_randoms_email')
    else:
        form = EmailRandomsNotificationForm()
        context = {
            'form': form
        }
        return render(request, 'hod_template/add_randoms_email_template.html', context)


@login_required(login_url='user_login')
def manage_randoms_email(request):
    emails = EmailRandomsNotification.objects.all()
    context = {
        "emails": emails
    }
    return render(request, 'hod_template/manage_randoms_email_template.html', context)


@login_required(login_url='user_login')
def add_notification_driver(request):
    drivers = Drivers.objects.all()
    context = {
        "drivers": drivers
    }
    return render(request, 'hod_template/add_driver_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_driver_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_driver')
    else:
        message = request.POST.get('message')

        driver_id = request.POST.get('driver')
        driver = Drivers.objects.get(id=driver_id)

        try:
            driver_notification = NotificationDriver(message=message, driver_id=driver)
            driver_notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_driver')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_driver')


@login_required(login_url='user_login')
def manage_notification_driver(request):
    notification_drivers = NotificationDriver.objects.all()
    context = {
        "notification_drivers": notification_drivers
    }
    return render(request, 'hod_template/manage_driver_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_driver(request, driver_id):
    request.session['driver_id'] = driver_id

    driver = Drivers.objects.get(id=driver_id)
    context = {
        "driver": driver,
        "id": driver_id
    }
    return render(request, 'hod_template/edit_driver_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_driver_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        driver_id = request.session.get('driver_id')
        message = request.POST.get('message')
        driver = Drivers.objects.get(id=driver_id)

        try:
            driver_notification = NotificationDriver(message=message, driver_id=driver)
            driver_notification.save()

            del request.session['driver_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('manage_user')

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('manage_user')
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_driver(request, notification_driver_id):
    notification_driver = NotificationDriver.objects.get(id=notification_driver_id)
    try:
        notification_driver.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_driver')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_driver')


@login_required(login_url='user_login')
def add_notification_owner(request):
    owners = Apartment_owners.objects.all()
    context = {
        "owners": owners
    }
    return render(request, 'hod_template/add_owner_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_owner_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_owner')
    else:
        message = request.POST.get('message')

        owner_id = request.POST.get('owner')
        owner = Apartment_owners.objects.get(id=owner_id)

        try:
            owner_notification = NotificationOwner(message=message, owner_id=owner)
            owner_notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_owner')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_owner')


@login_required(login_url='user_login')
def manage_notification_owner(request):
    notification_owners = NotificationOwner.objects.all()
    context = {
        "notification_owners": notification_owners
    }
    return render(request, 'hod_template/manage_owner_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_owner(request, owner_id):
    request.session['owner_id'] = owner_id

    owner = Apartment_owners.objects.get(id=owner_id)
    context = {
        "owner": owner,
        "id": owner_id
    }
    return render(request, 'hod_template/edit_owner_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_owner_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        owner_id = request.session.get('owner_id')
        message = request.POST.get('message')
        owner = Apartment_owners.objects.get(id=owner_id)

        try:
            owner_notification = NotificationOwner(message=message, owner_id=owner)
            owner_notification.save()

            del request.session['owner_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_staff/' + owner_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_staff/' + owner_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_owner(request, notification_owner_id):
    notification_owner = NotificationOwner.objects.get(id=notification_owner_id)
    try:
        notification_owner.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_owner')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_driver')


@login_required(login_url='user_login')
def add_notification_tenant(request):
    tenants = Tenants.objects.all()
    context = {
        "tenants": tenants
    }
    return render(request, 'hod_template/add_tenant_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_tenant_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_tenant')
    else:
        message = request.POST.get('message')

        tenant_id = request.POST.get('tenant')
        tenant = Tenants.objects.get(id=tenant_id)

        try:
            tenant_notification = NotificationTenant(message=message, tenant_id=tenant)
            tenant_notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_tenant')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_tenant')


@login_required(login_url='user_login')
def manage_notification_tenant(request):
    notification_tenants = NotificationTenant.objects.all()
    context = {
        "notification_tenants": notification_tenants
    }
    return render(request, 'hod_template/manage_tenant_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_tenant(request, tenant_id):
    request.session['tenant_id'] = tenant_id

    tenant = Tenants.objects.get(id=tenant_id)
    context = {
        "tenant": tenant,
        "id": tenant_id
    }
    return render(request, 'hod_template/edit_tenant_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_tenant_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        tenant_id = request.session.get('tenant_id')
        message = request.POST.get('message')
        tenant = Tenants.objects.get(id=tenant_id)

        try:
            tenant_notification = NotificationTenant(message=message, tenant_id=tenant)
            tenant_notification.save()

            del request.session['tenant_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_student/' + tenant_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_student/' + tenant_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_tenant(request, notification_tenant_id):
    notification_tenant = NotificationTenant.objects.get(id=notification_tenant_id)
    try:
        notification_tenant.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_tenant')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_tenant')


@login_required(login_url='user_login')
def requested_termination_view(request):
    terminations = RequestTermination.objects.all()
    context = {
        "terminations": terminations
    }
    return render(request, 'hod_template/contract_termination_view.html', context)


@login_required(login_url='user_login')
def swo_meeting_view(request):
    user = User.objects.get(id=request.user.id)
    admin = AdminHOD.objects.get(admin__user=user)
    office = admin.office
    swo_meetings = SWMeeting.objects.filter(office=office)
    context = {
        "swo_meetings": swo_meetings
    }
    return render(request, 'hod_template/swo_meeting_view.html', context)


@login_required(login_url='user_login')
def request_swo_meeting_view(request, termination_id):
    user = User.objects.get(id=request.user.id)
    admin = AdminHOD.objects.get(admin__user=user)
    office = admin.office
    termination_id = RequestTermination.objects.get(id=termination_id)
    termination = RequestTermination.objects.get(id=termination_id)
    owner_id = termination.owner_id
    tenant_id = termination.tenant_id
    apartment_id = termination.apartment_id
    reason = termination.reason
    applied_person = termination.applied_person

    swo_meeting = SWMeeting(owner_id=owner_id, tenant_id=tenant_id, apartment_id=apartment_id, status=0, office=office,
                            reason=reason, applied_person=applied_person, dec_reason="", decision= "")
    swo_meeting.save()
    return redirect('swo_meeting_view')


@login_required(login_url='user_login')
def requested_termination_approve(request, swo_meeting_id):
    swo_meeting = SWMeeting.objects.get(id=swo_meeting_id)
    owner_id = swo_meeting.owner_id
    tenant_id = swo_meeting.tenant_id
    apartment_id = swo_meeting.apartment_id
    reason = swo_meeting.reason
    applied_person = swo_meeting.applied_person
    termination = RequestTermination.objects.get(owner_id=owner_id, tenant_id=tenant_id, apartment_id=apartment_id,
                                                 reason=reason, applied_person=applied_person)
    termination.accepted = 1
    apartment_obj = termination.apartment_id
    apartment_obj.is_visible = True
    apartment_obj.save()
    termination.save()
    return redirect('requested_termination_view')


@login_required(login_url='user_login')
def requested_termination_reject2(request, swo_meeting_id):
    swo_meeting = SWMeeting.objects.get(id=swo_meeting_id)
    owner_id = swo_meeting.owner_id
    tenant_id = swo_meeting.tenant_id
    apartment_id = swo_meeting.apartment_id
    reason = swo_meeting.reason
    applied_person = swo_meeting.applied_person
    termination = RequestTermination.objects.get(owner_id=owner_id, tenant_id=tenant_id, apartment_id=apartment_id,
                                                 reason=reason, applied_person=applied_person)
    termination.accepted = 2
    termination.save()
    return redirect('requested_termination_view')


@login_required(login_url='user_login')
def requested_termination_reject(request, termination_id):
    termination = RequestTermination.objects.get(id=termination_id)
    termination.accepted = 2
    termination.save()
    return redirect('requested_termination_view')


@login_required(login_url='user_login')
def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year_id")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    # students = Students.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)
    attendance = Attendance.objects.filter(subject_id=subject_model, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for attendance_single in attendance:
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    # Getting Values from Ajax POST 'Fetch Student'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Student Id and Student Name Only
    list_data = []

    for tenant in attendance_data:
        data_small={"id":tenant.tenant_id.admin.id, "name":tenant.tenant_id.admin.user.first_name+" "+tenant.tenant_id.admin.user.last_name, "status":tenant.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@login_required(login_url='user_login')
def admin_profile(request):
    user = User.objects.get(id=request.user.id)
    admin = AdminHOD.objects.get(admin__user=user)
    context={
        "user": user,
        "admin": admin,
    }
    return render(request, 'hod_template/admin_profile.html', context)


@login_required(login_url='user_login')
def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(id=request.user.id)
            customuser = AdminHOD.objects.get(admin__user=user)
            customuser.user.first_name = first_name
            customuser.user.last_name = last_name
            customuser.user.email = email
            customuser.user.username = username
            if password != None and password != "":
                customuser.user.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')


@login_required(login_url='user_login')
def staff_add_result(request):
    apartments = Album.objects.all()
    session_years = SessionYearModel.objects.all()
    tenants = CustomUser.objects.filter(user_type='3')
    context = {
        "apartments": apartments,
        "session_years": session_years,
        "tenants": tenants,
    }
    return render(request, "hod_template/add_result_template.html", context)


@login_required(login_url='user_login')
def staff_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:

        apartment_marks = request.POST.get('apartment_marks')
        apartment_exam_marks = request.POST.get('apartment_exam_marks')
        apartment_id = request.POST.get('apartment')
        tenant_id = request.POST.get('tenant')

        tenant_obj = Tenants.objects.get(id=tenant_id)
        apartment_obj = Album.objects.get(id=apartment_id)

        try:
            # Check if Students Result Already Exists or not
            check_exist = ApartmentResult.objects.filter(apartment_id=apartment_obj).exists()
            if check_exist:
                result = ApartmentResult.objects.get(apartment_id=apartment_obj)
                result.apartment_assignment_marks = apartment_marks
                result.apartment_exam_marks = apartment_exam_marks
                result.apartment_id = apartment_obj
                if int(apartment_exam_marks) >= 70:
                    apartment_obj.is_visible = False
                    apartment_obj.save()
                else:
                    apartment_obj.quantity += 1
                    apartment_obj.is_visible = True
                    apartment_obj.save()
                result.tenant_id = tenant_obj
                result.save()
                messages.success(request, "Result Updated Successfully!")
                return redirect('staff_add_result')
            else:
                if int(apartment_exam_marks) >= 70:
                    if apartment_obj.quantity >= 1:
                        apartment_obj.quantity -= 1
                        apartment_obj.is_visible = True
                        apartment_obj.save()
                    else:
                        apartment_obj.is_visible = False
                        apartment_obj.save()
                else:
                    apartment_obj.is_visible = True
                    apartment_obj.save()
                result = ApartmentResult(apartment_id=apartment_obj, tenant_id=tenant_obj,
                                         apartment_exam_marks=apartment_exam_marks,
                                         apartment_assignment_marks=apartment_marks)
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('staff_add_result')
        except:
            messages.error(request, "Failed to Add Result!")
            return redirect('staff_add_result')


@login_required(login_url='user_login')
def visible(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_add_result')
    else:
        apartment_exam_marks = request.POST.get('apartment_exam_marks')
        apartment_id = request.POST.get('apartment')

        apartment_obj = Album.objects.get(id=apartment_id)
        if int(apartment_exam_marks) <= 70:
            apartment_obj.is_visible = False
            apartment_obj.save()
            return redirect('staff_add_result')
        else:
            apartment_obj.is_visible = True
            apartment_obj.save()
            return redirect('staff_add_result')


@csrf_exempt
def get_tenants(request):
    # Getting Values from Ajax POST 'Fetch Student'

    session_year = request.POST.get("session_year")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id


    session_model = SessionYearModel.objects.get(id=session_year)

    tenants = Tenants.objects.filter(session_year_id=session_model)


    # Only Passing Student Id and Student Name Only
    list_data = []


    for tenant in tenants:
        data_small={"id":tenant.id, "name":tenant.admin.user.first_name+" "+tenant.admin.user.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_apartments(request):
    # Getting Values from Ajax POST 'Fetch Student'

    session_year = request.POST.get("session_year")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id


    session_model = SessionYearModel.objects.get(id=session_year)

    apartments = Album.objects.filter(session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data2 = []


    for apartment in apartments:
        data_small2={"id":apartment.id, "name":apartment.title+" "+apartment.spec_location}
        list_data2.append(data_small2)

    return JsonResponse(json.dumps(list_data2), content_type="application/json", safe=False)


@login_required(login_url='user_login')
def staff_profile(request):
    pass


@login_required(login_url='user_login')
def student_profile(request):
    pass



