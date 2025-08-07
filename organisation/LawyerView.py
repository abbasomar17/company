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
from .forms import *


@login_required(login_url='login')
def law_home(request):
    user = User.objects.get(id=request.user.id)
    law_obj = S_CustomUser.objects.get(user=user)
    met_obj = Lawyers.objects.get(admin=law_obj)
    no_lawyer = Lawyers.objects.all().count()
    no_office = Office.objects.all().count()
    if Office.objects.all().exists():
        ratio = no_lawyer/no_office
    else:
        ratio = 0
    total_hr_attendance = AttendanceHRReport.objects.filter(attendant_id=law_obj).count()
    attendance_hr_present = AttendanceHRReport.objects.filter(attendant_id=law_obj, status=1).count()
    attendance_hr_absent = AttendanceHRReport.objects.filter(attendant_id=law_obj, status=2).count()
    total_ceo_attendance = AttendanceCEOReport.objects.filter(attendant_id=law_obj).count()
    attendance_ceo_present = AttendanceCEOReport.objects.filter(attendant_id=law_obj, status=1).count()
    attendance_ceo_absent = AttendanceCEOReport.objects.filter(attendant_id=law_obj, status=2).count()

    meeting_ceo_name = []
    data_ceo_present = []
    data_ceo_absent = []
    meeting_ceo_data = CEOMeeting.objects.all()
    for subject in meeting_ceo_data:
        attendance_present_count = AttendanceCEOReport.objects.filter(meeting_id=subject.id, status=1,
                                                                      attendant_id=law_obj.id).count()
        attendance_absent_count = AttendanceCEOReport.objects.filter(meeting=subject.id, status=2,
                                                                     attendant_id=law_obj.id).count()
        meeting_ceo_name.append(subject.meeting_name)
        data_ceo_present.append(attendance_present_count)
        data_ceo_absent.append(attendance_absent_count)

    meeting_hr_name = []
    data_hr_present = []
    data_hr_absent = []

    meeting_hr_data = HRMeeting.objects.all()
    for subject in meeting_hr_data:
        attendance_present_count = AttendanceHRReport.objects.filter(meeting=subject.id, status=1,
                                                                     attendant_id=law_obj.id).count()
        attendance_absent_count = AttendanceHRReport.objects.filter(meeting_id=subject.id, status=1,
                                                                    attendant_id=law_obj.id).count()
        meeting_hr_name.append(subject.meeting_name)
        data_hr_present.append(attendance_present_count)
        data_hr_absent.append(attendance_absent_count)

    context = {
        "total_hr_attendance": total_hr_attendance,
        "attendance_hr_present": attendance_hr_present,
        "attendance_hr_absent": attendance_hr_absent,
        "total_ceo_attendance": total_ceo_attendance,
        "attendance_ceo_present": attendance_ceo_present,
        "attendance_ceo_absent": attendance_ceo_absent,
        "no_office": no_office,
        "no_lawyer": no_lawyer,
        "ratio": ratio,
        "meeting_ceo_name": meeting_ceo_name,
        "data_ceo_present": data_ceo_present,
        "data_ceo_absent": data_ceo_absent,
        "meeting_hr_name": meeting_hr_name,
        "data_hr_present": data_hr_present,
        "data_hr_absent": data_hr_absent
    }
    return render(request, "law_template/law_home_template.html", context)


@login_required(login_url='user_login')
def law_view_ceo_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceCEOReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'law_template/law_ceo_attendance.html', context)


@login_required(login_url='user_login')
def law_view_hr_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceHRReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'law_template/law_hr_attendance.html', context)


@login_required(login_url='user_login')
def law_feedback(request):
    user = User.objects.get(id=request.user.id)
    law_obj = Lawyers.objects.get(admin__user=user)
    feedback_data = FeedBackLawyer.objects.filter(lawyer_id=law_obj)
    offices = Office.objects.all()
    context = {
        "feedback_data": feedback_data,
        "offices": offices
    }
    return render(request, 'law_template/law_feedback.html', context)


@login_required(login_url='user_login')
def law_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('law_feedback')
    else:
        office_id = request.POST.get('office')
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        law_obj = Lawyers.objects.get(admin__user=user)

        office = Office.objects.get(id=office_id)

        try:
            add_feedback = FeedBackLawyer(lawyer_id=law_obj, office=office, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('law_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('law_feedback')


@login_required(login_url='user_login')
def law_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    law_obj = Lawyers.objects.get(admin__user=user)
    leave_data = LeaveReportLawyer.objects.filter(lawyer_id=law_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'law_template/law_apply_leave.html', context)


@login_required(login_url='user_login')
def law_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('law_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        law_obj = Lawyers.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportLawyer(lawyer_id=law_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('law_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('law_apply_leave')


@login_required(login_url='user_login')
def law_apply_permission(request):
    user = User.objects.get(id=request.user.id)
    law_obj = Lawyers.objects.get(admin__user=user)
    permission_data = PermissionReportLawyer.objects.filter(lawyer_id=law_obj)
    context = {
        "permission_data": permission_data
    }
    return render(request, 'law_template/law_apply_permission.html', context)


@login_required(login_url='user_login')
def law_apply_permission_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('law_permission_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        law_obj = Lawyers.objects.get(admin__user=user)
        try:
            leave_report = PermissionReportLawyer(lawyer_id=law_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Permission.")
            return redirect('law_apply_permission')
        except:
            messages.error(request, "Failed to Apply Permission")
            return redirect('law_apply_permission')


@login_required(login_url='user_login')
def law_view_notification(request):
    user = User.objects.get(id=request.user.id)
    law = Lawyers.objects.get(admin__user=user)
    notifications = NotificationLawyer.objects.filter(lawyer_id=law.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "law_template/law_view_notification.html", context)


@login_required(login_url='user_login')
def law_view_def_notification(request):
    user = User.objects.get(id=request.user.id)
    law = Lawyers.objects.get(admin__user=user)
    def_notifications = DefendantNotificationLawyer.objects.filter(lawyer_id=law.id)
    context = {
        "notifications": def_notifications,
    }
    return render(request, "law_template/law_view_def_notification.html", context)


@login_required(login_url='user_login')
def law_view_acu_notification(request):
    user = User.objects.get(id=request.user.id)
    law = Lawyers.objects.get(admin__user=user)
    acu_notifications = AccusserNotificationLawyer.objects.filter(lawyer_id=law.id)
    context = {
        "notifications": acu_notifications,
    }
    return render(request, "law_template/law_view_acu_notification.html", context)


@login_required(login_url='user_login')
def law_profile(request):
    user = User.objects.get(id=request.user.id)
    law_obj = Lawyers.objects.get(admin__user=user)
    context={
        "user": user,
        "law": law_obj,
    }
    return render(request, 'law_template/law_profile.html', context)


@login_required(login_url='user_login')
def law_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('law_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.get(id=request.user.id)
            ceo_obj = Lawyers.objects.get(admin__user=user)
            customuser = S_CustomUser.objects.get(user=user)
            customuser.user.first_name = first_name
            customuser.user.last_name = last_name
            customuser.user.email = email
            customuser.user.username = username
            if password != None and password != "":
                customuser.user.set_password(password)
            customuser.save()
            ceo_obj.address = address
            ceo_obj.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('law_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('law_profile')


@login_required(login_url='user_login')
def my_view_law_resp(request):
    obj = User.objects.get(id=request.user.id)
    user_obj = Lawyers.objects.get(admin__user=obj)
    office = user_obj.office
    resps = ResponsibilityLawyers.objects.all()
    context = {
        "resps": resps
    }
    return render(request, 'law_template/view_law_resp.html', context)