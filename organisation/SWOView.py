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


@login_required(login_url='user_login')
def swo_home(request):
    user = User.objects.get(id=request.user.id)
    swo_obj = S_CustomUser.objects.get(user=user)
    met_obj = Social_welfare_officers.objects.get(admin=swo_obj)
    office = met_obj.office
    pending_sw_meetings = SWMeeting.objects.filter(office=office, status=0).count()
    arranged_sw_meetings = SWMeeting.objects.filter(office=office, status=1).count()
    concluded_sw_meetings = SWMeeting.objects.filter(office=office, status=2).count()
    all_sw_meetings = SWMeeting.objects.filter(office=office).count()
    total_hr_attendance = AttendanceHRReport.objects.filter(attendant_id=swo_obj).count()
    attendance_hr_present = AttendanceHRReport.objects.filter(attendant_id=swo_obj, status=1).count()
    attendance_hr_absent = AttendanceHRReport.objects.filter(attendant_id=swo_obj, status=2).count()
    total_ceo_attendance = AttendanceCEOReport.objects.filter(attendant_id=swo_obj).count()
    attendance_ceo_present = AttendanceCEOReport.objects.filter(attendant_id=swo_obj, status=1).count()
    attendance_ceo_absent = AttendanceCEOReport.objects.filter(attendant_id=swo_obj, status=2).count()

    meeting_ceo_name = []
    data_ceo_present = []
    data_ceo_absent = []
    meeting_ceo_data = CEOMeeting.objects.filter(office=met_obj.office)
    for subject in meeting_ceo_data:
        attendance_present_count = AttendanceCEOReport.objects.filter(meeting_id=subject.id, status=1,
                                                                   attendant_id=swo_obj.id).count()
        attendance_absent_count = AttendanceCEOReport.objects.filter(meeting=subject.id, status=2,
                                                                  attendant_id=swo_obj.id).count()
        meeting_ceo_name.append(subject.meeting_name)
        data_ceo_present.append(attendance_present_count)
        data_ceo_absent.append(attendance_absent_count)

    meeting_hr_name = []
    data_hr_present = []
    data_hr_absent = []

    meeting_hr_data = HRMeeting.objects.filter(office=met_obj.office)
    for subject in meeting_hr_data:
        attendance_present_count = AttendanceHRReport.objects.filter(meeting=subject.id, status=1,
                                                                      attendant_id=swo_obj.id).count()
        attendance_absent_count = AttendanceHRReport.objects.filter(meeting_id=subject.id, status=1,
                                                                     attendant_id=swo_obj.id).count()
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
        "all_sw_meetings": all_sw_meetings,
        "arranged_sw_meetings": arranged_sw_meetings,
        "concluded_sw_meetings": concluded_sw_meetings,
        "pending_sw_meetings": pending_sw_meetings,
        "meeting_ceo_name": meeting_ceo_name,
        "data_ceo_present": data_ceo_present,
        "data_ceo_absent": data_ceo_absent,
        "meeting_hr_name": meeting_hr_name,
        "data_hr_present": data_hr_present,
        "data_hr_absent": data_hr_absent
    }
    return render(request, "swo_template/swo_home_template.html", context)


@login_required(login_url='user_login')
def swo_view_ceo_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceCEOReport.objects.filter(attendant_id = obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'swo_template/swo_ceo_attendance.html', context)


@login_required(login_url='user_login')
def swo_view_hr_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceHRReport.objects.filter(attendant_id = obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'swo_template/swo_hr_attendance.html', context)


@login_required(login_url='user_login')
def swo_feedback(request):
    user = User.objects.get(id=request.user.id)
    swo_obj = Social_welfare_officers.objects.get(admin__user=user)
    feedback_data = FeedBackSWO.objects.filter(swo_id=swo_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'swo_template/swo_feedback.html', context)


@login_required(login_url='user_login')
def swo_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('swo_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        swo_obj = Social_welfare_officers.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackSWO(swo_id=swo_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('swo_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('swo_feedback')


@login_required(login_url='user_login')
def swo_sw_meeting_view(request):
    user = User.objects.get(id=request.user.id)
    swo = Social_welfare_officers.objects.get(admin__user=user)
    office = swo.office
    swo_meetings = SWMeeting.objects.filter(office=office, status=0)
    context = {
        "swo_meetings": swo_meetings
    }
    return render(request, 'swo_template/swo_meeting_view.html', context)


@login_required(login_url='user_login')
def arrange_sw_meeting_view(request, swo_meeting_id):
    request.session['swo_meeting_id'] = swo_meeting_id
    swo_meeting = SWMeeting.objects.get(id=swo_meeting_id)
    context = {
        "swo_meeting": swo_meeting,
        "id": swo_meeting_id
    }

    return render(request, 'swo_template/arrange_sw_meeting_view.html', context)


@login_required(login_url='user_login')
def arrange_sw_meeting_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        swo_meeting_id = request.session.get('swo_meeting_id')
        date = request.POST.get('date')
        swo_meeting = SWMeeting.objects.get(id=swo_meeting_id)
        try:
            swo_meeting.date = date
            swo_meeting.status = 1
            swo_meeting.save()

            del request.session['swo_meeting_id']
            messages.success(request, "SW Meeting Was Arranged Successfully!")
            return redirect('arrange_sw_meeting_view')
        except:
            messages.error(request, "Failed to Arrange SW Meeting.")
            return redirect('arrange_sw_meeting_view')


@login_required(login_url='user_login')
def arranged_sw_meeting_view(request):
    user = User.objects.get(id=request.user.id)
    swo = Social_welfare_officers.objects.get(admin__user=user)
    office = swo.office
    swo_meetings = SWMeeting.objects.filter(office=office, status=1)
    context = {
        "swo_meetings": swo_meetings
    }
    return render(request, 'swo_template/arranged_sw_meeting_view.html', context)


@login_required(login_url='user_login')
def conclude_sw_meeting_view(request, swo_meeting_id):
    request.session['swo_meeting_id'] = swo_meeting_id
    swo_meeting = SWMeeting.objects.get(id=swo_meeting_id)
    context = {
        "swo_meeting": swo_meeting,
        "id": swo_meeting_id
    }

    return render(request, 'swo_template/conclude_sw_meeting_view.html', context)


@login_required(login_url='user_login')
def conclude_sw_meeting_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        swo_meeting_id = request.session.get('swo_meeting_id')
        decision = request.POST.get('decision')
        dec_reason = request.POST.get('reason')
        swo_meeting = SWMeeting.objects.get(id=swo_meeting_id)
        try:
            swo_meeting.decision = decision
            swo_meeting.dec_reason = dec_reason
            swo_meeting.status = 2
            swo_meeting.save()

            del request.session['swo_meeting_id']
            messages.success(request, "SW Meeting Was Concluded Successfully!")
            return redirect('conclude_sw_meeting_view')
        except:
            messages.error(request, "Failed to Conclude SW Meeting.")
            return redirect('conclude_sw_meeting_view')


@login_required(login_url='user_login')
def concluded_sw_meeting_view(request):
    user = User.objects.get(id=request.user.id)
    swo = Social_welfare_officers.objects.get(admin__user=user)
    office = swo.office
    swo_meetings = SWMeeting.objects.filter(office=office, status=2)
    context = {
        "swo_meetings": swo_meetings
    }
    return render(request, 'swo_template/concluded_sw_meeting_view.html', context)


@login_required(login_url='user_login')
def swo_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    swo_obj = Social_welfare_officers.objects.get(admin__user=user)
    leave_data = LeaveReportSWO.objects.filter(swo_id=swo_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'swo_template/swo_apply_leave.html', context)


@login_required(login_url='user_login')
def swo_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('swo_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        swo_obj = Social_welfare_officers.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportSWO(swo_id=swo_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('swo_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('swo_apply_leave')


@login_required(login_url='user_login')
def swo_apply_permission(request):
    user = User.objects.get(id=request.user.id)
    swo_obj = Social_welfare_officers.objects.get(admin__user=user)
    permission_data = PermissionReportSWO.objects.filter(swo_id=swo_obj)
    context = {
        "permission_data": permission_data
    }
    return render(request, 'swo_template/swo_apply_permission.html', context)


@login_required(login_url='user_login')
def swo_apply_permission_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('swo_permission_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        swo_obj = Social_welfare_officers.objects.get(admin__user=user)
        try:
            leave_report = PermissionReportSWO(swo_id=swo_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('swo_apply_permission')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('swo_apply_permission')


@login_required(login_url='user_login')
def swo_view_notification(request):
    user = User.objects.get(id=request.user.id)
    swo = Social_welfare_officers.objects.get(admin__user=user)
    notifications = NotificationSWO.objects.filter(swo_id=swo.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "swo_template/swo_view_notification.html", context)


@login_required(login_url='user_login')
def swo_view_def_notification(request):
    user = User.objects.get(id=request.user.id)
    swo = Social_welfare_officers.objects.get(admin__user=user)
    def_notifications = DefendantNotificationSWO.objects.filter(swo_id=swo.id)
    context = {
        "notifications": def_notifications,
    }
    return render(request, "swo_template/swo_view_def_notification.html", context)


@login_required(login_url='user_login')
def swo_view_acu_notification(request):
    user = User.objects.get(id=request.user.id)
    swo = Social_welfare_officers.objects.get(admin__user=user)
    acu_notifications = AccusserNotificationSWO.objects.filter(swo_id=swo.id)
    context = {
        "notifications": acu_notifications,
    }
    return render(request, "swo_template/swo_view_acu_notification.html", context)


@login_required(login_url='user_login')
def swo_profile(request):
    user = User.objects.get(id=request.user.id)
    swo_obj = Social_welfare_officers.objects.get(admin__user=user)
    context={
        "user": user,
        "swo": swo_obj,
    }
    return render(request, 'swo_template/swo_profile.html', context)


@login_required(login_url='user_login')
def swo_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('swo_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.get(id=request.user.id)
            ceo_obj = Social_welfare_officers.objects.get(admin__user=user)
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
            return redirect('swo_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('swo_profile')


@login_required(login_url='user_login')
def my_view_swo_resp(request):
    obj = User.objects.get(id=request.user.id)
    user_obj = Social_welfare_officers.objects.get(admin__user=obj)
    office = user_obj.office
    resps = ResponsibilitySWO.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'swo_template/view_swo_resp.html', context)


