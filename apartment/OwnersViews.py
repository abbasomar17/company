from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import *
from .forms import AddTenantForm, EditTenantForm, AddDriverForm, EditDriverForm, AddCustomerForm, AddOwnerForm


@login_required(login_url='login')
def staff_home(request):
    user = User.objects.get(id=request.user.id)
    all_tenant_count = Tenants.objects.filter(owner_id__admin__user=user).count()

    # For Students
    tenant_name_list = []

    tenants = Tenants.objects.all()
    for tenant in tenants:
        tenant_name_list.append(tenant.admin.user.first_name)
    # Fetching All Students under Staff

    subjects = Subjects.objects.filter(owner_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    
    final_course = []
    # Removing Duplicate Course Id
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)
    
    tenants_count = Tenants.objects.filter(course_id__in=final_course).count()
    subject_count = subjects.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    # Fetch All Approve Leave
    owner = Apartment_owners.objects.get(admin__user=user)
    leave_count = LeaveReportOwner.objects.filter(owner_id=owner.id, leave_status=1).count()

    #Fetch Attendance Data by Subjects
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    tenants_attendance = Tenants.objects.filter(course_id__in=final_course)
    tenant_list = []
    tenant_list_attendance_present = []
    tenant_list_attendance_absent = []
    for tenant in tenants_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, tenant_id=tenant.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, tenant_id=tenant.id).count()
        tenant_list.append(tenant.admin.user.first_name+" "+ tenant.admin.user.last_name)
        tenant_list_attendance_present.append(attendance_present_count)
        tenant_list_attendance_absent.append(attendance_absent_count)

    context={
        "all_tenant_count": all_tenant_count,
        "tenant_name_list": tenant_name_list,
        "tenants_count": tenants_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "subject_count": subject_count,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "tenant_list": tenant_list,
        "attendance_present_list": tenant_list_attendance_present,
        "attendance_absent_list": tenant_list_attendance_absent
    }
    return render(request, "staff_template/staff_home_template.html", context)


@login_required(login_url='login')
def staff_take_attendance(request):
    subjects = Subjects.objects.filter(owner_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/take_attendance_template.html", context)


@login_required(login_url='login')
def staff_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    owner_obj = Apartment_owners.objects.get(admin__user=user)
    leave_data = LeaveReportOwner.objects.filter(owner_id=owner_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "staff_template/staff_apply_leave_template.html", context)


@login_required(login_url='login')
def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        user = User.objects.get(id=request.user.id)
        owner_obj = Apartment_owners.objects.get(admin__user=request.user.id)
        try:
            leave_report = LeaveReportOwner(owner_id=owner_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


@login_required(login_url='login')
def staff_feedback(request):
    user = User.objects.get(id=request.user.id)
    owner_obj = Apartment_owners.objects.get(admin__user=user)
    feedback_data = FeedBackOwner.objects.filter(owner_id=owner_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_template/staff_feedback_template.html", context)


@login_required(login_url='login')
def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        owner_obj = Apartment_owners.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackOwner(owner_id=owner_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_students(request):
    # Getting Values from Ajax POST 'Fetch Student'
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id
    subject_model = Subjects.objects.get(id=subject_id)

    session_model = SessionYearModel.objects.get(id=session_year)

    tenants = Tenants.objects.filter(course_id=subject_model.course_id, session_year_id=session_model)

    # Only Passing Student Id and Student Name Only
    list_data = []

    for tenant in tenants:
        data_small={"id":tenant.admin.id, "name":tenant.admin.user.first_name+" "+tenant.admin.user.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)




@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staff Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    tenant_ids = request.POST.get("tenant_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_year_model = SessionYearModel.objects.get(id=session_year_id)

    json_tenant = json.loads(tenant_ids)
    # print(dict_student[0]['id'])

    # print(student_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date, session_year_id=session_year_model)
        attendance.save()

        for tent in json_tenant:
            # Attendance of Individual Student saved on AttendanceReport Model
            tenant = Tenants.objects.get(admin=tent['id'])
            attendance_report = AttendanceReport(tenant_id=tenant, attendance_id=attendance, status=tent['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")



@login_required(login_url='login')
def staff_update_attendance(request):
    subjects = Subjects.objects.filter(owner_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "staff_template/update_attendance_template.html", context)


@csrf_exempt
def get_attendance_dates(request):
    

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
def get_attendance_student(request):
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


@csrf_exempt
def update_attendance_data(request):
    tenant_ids = request.POST.get("tenants_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_tenant = json.loads(tenant_ids)

    try:
        
        for tent in json_tenant:
            # Attendance of Individual Student saved on AttendanceReport Model
            tenant = Tenants.objects.get(admin=tent['id'])

            attendance_report = AttendanceReport.objects.get(tenant_id=tenant, attendance_id=attendance)
            attendance_report.status=tent['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


@login_required(login_url='login')
def staff_profile(request):
    user = User.objects.get(id=request.user.id)
    owner = Apartment_owners.objects.get(admin__user=user)

    context={
        "user": user,
        "owner": owner
    }
    return render(request, 'staff_template/staff_profile.html', context)


@login_required(login_url='login')
def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.get(id=request.user.id)
            customuser = CustomUser.objects.get(user=user)
            customuser.user.first_name = first_name
            customuser.user.last_name = last_name
            customuser.user.username = username
            customuser.user.email = email
            if password != None and password != "":
                customuser.user.set_password(password)
            customuser.save()

            owner = Apartment_owners.objects.get(admin=customuser.id)
            owner.address = address
            owner.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')

@login_required(login_url='login')
def staff_view_result(request):
    user = User.objects.get(id=request.user.id)
    owner = Apartment_owners.objects.get(admin__user=user)
    apartment_result = ApartmentResult.objects.filter(apartment_id__owner_id=owner.id)
    context = {
        "apartment_result": apartment_result,
    }
    return render(request, "staff_template/staff_view_result.html", context)


@login_required(login_url='login')
def owner_request_termination(request):
    user = User.objects.get(id=request.user.id)
    owner_obj = Apartment_owners.objects.get(admin__user=user)
    termination_data = RequestTermination.objects.filter(owner_id=owner_obj)
    apartments = Album.objects.filter(owner_id=owner_obj)
    context = {
        "termination_data": termination_data,
        "apartments": apartments
    }
    return render(request, "staff_template/owner_termination_template.html", context)


@login_required(login_url='login')
def owner_request_termination_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('owner_request_termination')
    else:
        reason = request.POST.get('reason')
        apartment_id = request.POST.get('apartment')
        tenant_id = request.POST.get('tenant')

        user = User.objects.get(id=request.user.id)
        owner_obj = Apartment_owners.objects.get(admin__user=user)
        tenant_obj = Tenants.objects.get(id=tenant_id)
        apartment_obj = Album.objects.get(id=apartment_id)

        try:
            check_exist = RequestTermination.objects.filter(tenant_id=tenant_obj).exists()
            if check_exist:
                termination = RequestTermination.objects.get(tenant_id=tenant_obj)
                termination.reason = reason
                termination.owner_id = owner_obj
                termination.apartment_id = apartment_obj
                termination.tenant_id = tenant_obj
                termination.accepted = 0
                if termination.applied_person == "Tenant":
                    termination.applied_person = "Both"
                else:
                    termination.applied_person = "Owner"

                termination.save()
                messages.success(request, "Termination Request Updated.")
                return redirect('owner_request_termination')
            else:
                termination = RequestTermination(reason=reason, tenant_id=tenant_obj, apartment_id=apartment_obj, owner_id=owner_obj, applied_person="Owner", accepted=0)
                termination.save()
                messages.success(request, "Termination Request Sent.")
                return redirect('owner_request_termination')
        except:
            messages.error(request, "Failed to Send Termination Request.")
            return redirect('owner_request_termination')


@login_required(login_url='login')
def owner_view_notification(request):
    user = User.objects.get(id=request.user.id)
    owner = Apartment_owners.objects.get(admin__user=user)
    notifications = NotificationOwner.objects.filter(owner_id=owner.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "staff_template/owner_view_notification.html", context)


@csrf_exempt
def get_tenants2(request):
    # Getting Values from Ajax POST 'Fetch Student'

    apartment = request.POST.get("apartment")

    # Students enroll to Course, Course has Subjects
    # Getting all data from subject model based on subject_id


    apartment_obj = Album.objects.get(id=apartment)

    tenants = Tenants.objects.filter(apartment_id=apartment_obj)


    # Only Passing Student Id and Student Name Only
    list_data4 = []


    for tenant in tenants:
        data_small4={"id":tenant.id, "name":tenant.admin.user.first_name+" "+tenant.admin.user.last_name}
        list_data4.append(data_small4)

    return JsonResponse(json.dumps(list_data4), content_type="application/json", safe=False)

