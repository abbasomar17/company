from django.shortcuts import render, redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object

from .models import *
from .forms import AddTenantForm, EditTenantForm, AddDriverForm, EditDriverForm, AddCustomerForm, AddOwnerForm


@login_required(login_url='login')
def student_home(request):
    user = User.objects.get(id=request.user.id)
    tenant_obj = Tenants.objects.get(admin__user=user)
    total_attendance = AttendanceReport.objects.filter(tenant_id=tenant_obj).count()
    attendance_present = AttendanceReport.objects.filter(tenant_id=tenant_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(tenant_id=tenant_obj, status=False).count()

    course_obj = Courses.objects.get(id=tenant_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=tenant_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, tenant_id=tenant_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, tenant_id=tenant_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    context={
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student_template/student_home_template.html", context)


@login_required(login_url='login')
def student_view_attendance(request):
    user = User.objects.get(id=request.user.id)
    tenant = Tenants.objects.get(admin__user=user) # Getting Logged in Student Data
    course = tenant.course_id # Getting Course Enrolled of LoggedIn Student
    # course = Courses.objects.get(id=student.course_id.id) # Getting Course Enrolled of LoggedIn Student
    subjects = Subjects.objects.filter(course_id=course) # Getting the Subjects of Course Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


@login_required(login_url='login')
def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(user__id=request.user.id)
        # Getting Student Data Based on Logged in Data
        tent_obj = Tenants.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, tenant_id=tent_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendance View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)
       

@login_required(login_url='login')
def student_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    tenant_obj = Tenants.objects.get(admin__user=user)
    leave_data = LeaveReportTenant.objects.filter(tenant_id=tenant_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)


@login_required(login_url='login')
def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        tenant_obj = Tenants.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportTenant(tenant_id=tenant_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


@login_required(login_url='login')
def student_feedback(request):
    user = User.objects.get(id=request.user.id)
    tenant_obj = Tenants.objects.get(admin__user=user)
    feedback_data = FeedBackTenant.objects.filter(tenant_id=tenant_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


@login_required(login_url='login')
def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        tenant_obj = Tenants.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackTenant(tenant_id=tenant_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


@login_required(login_url='login')
def student_profile(request):
    user = User.objects.get(id=request.user.id)
    tenant = Tenants.objects.get(admin__user=user)

    context={
        "user": user,
        "tenant": tenant
    }
    return render(request, 'student_template/student_profile.html', context)


@login_required(login_url='login')
def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        password = request.POST.get('password')

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

            tenant = Tenants.objects.get(admin=customuser.id)
            tenant.address = address
            tenant.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


@login_required(login_url='login')
def student_view_result(request):
    user = User.objects.get(id=request.user.id)
    tenant = Tenants.objects.get(admin__user=user)
    apartment_result = ApartmentResult.objects.filter(tenant_id=tenant.id)
    context = {
        "apartment_result": apartment_result,
    }
    return render(request, "student_template/student_view_result.html", context)


@login_required(login_url='login')
def tenant_view_notification(request):
    user = User.objects.get(id=request.user.id)
    tenant = Tenants.objects.get(admin__user=user)
    notifications = NotificationTenant.objects.filter(tenant_id=tenant.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "student_template/tenant_view_notification.html", context)


@login_required(login_url='login')
def tenant_request_termination(request):
    user = User.objects.get(id=request.user.id)
    tenant_obj = Tenants.objects.get(admin__user=user)
    termination_data = RequestTermination.objects.filter(tenant_id=tenant_obj)
    context = {
        "termination_data": termination_data
    }
    return render(request, 'student_template/tenant_termination.html', context)


@login_required(login_url='login')
def tenant_request_termination_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('tenant_request_termination')
    else:
        reason = request.POST.get('reason')
        user = User.objects.get(id=request.user.id)
        tenant_obj = Tenants.objects.get(admin__user=user)
        apartment_obj = tenant_obj.apartment_id
        owner_obj = apartment_obj.owner_id

        try:
            add_termination = RequestTermination(reason=reason, tenant_id=tenant_obj, apartment_id=apartment_obj, owner_id=owner_obj, applied_person="Tenant", accepted=0)
            add_termination.save()
            messages.success(request, "Termination Request Sent.")
            return redirect('tenant_request_termination')
        except:
            messages.error(request, "Failed to Send Termination Request.")
            return redirect('tenant_request_termination')
