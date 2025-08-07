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
def cs_home(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = S_CustomUser.objects.get(user=user)
    met_obj = Customer_service.objects.get(admin=cs_obj)
    my_reply = FeedBack.objects.filter(replied_by=met_obj).count()
    all_feedbacks = FeedBack.objects.filter(office=met_obj.office).count()
    all_unreplied_feedbacks = FeedBack.objects.filter(office=met_obj.office, feedback_reply="").count()
    all_replied_feedbacks = all_feedbacks - all_unreplied_feedbacks
    total_hr_attendance = AttendanceHRReport.objects.filter(attendant_id=cs_obj).count()
    attendance_hr_present = AttendanceHRReport.objects.filter(attendant_id=cs_obj, status=1).count()
    attendance_hr_absent = AttendanceHRReport.objects.filter(attendant_id=cs_obj, status=2).count()
    total_ceo_attendance = AttendanceCEOReport.objects.filter(attendant_id=cs_obj).count()
    attendance_ceo_present = AttendanceCEOReport.objects.filter(attendant_id=cs_obj, status=1).count()
    attendance_ceo_absent = AttendanceCEOReport.objects.filter(attendant_id=cs_obj, status=2).count()

    meeting_ceo_name = []
    data_ceo_present = []
    data_ceo_absent = []
    meeting_ceo_data = CEOMeeting.objects.filter(office=met_obj.office)
    for subject in meeting_ceo_data:
        attendance_present_count = AttendanceCEOReport.objects.filter(meeting_id=subject.id, status=1,
                                                                      attendant_id=cs_obj.id).count()
        attendance_absent_count = AttendanceCEOReport.objects.filter(meeting=subject.id, status=2,
                                                                     attendant_id=cs_obj.id).count()
        meeting_ceo_name.append(subject.meeting_name)
        data_ceo_present.append(attendance_present_count)
        data_ceo_absent.append(attendance_absent_count)

    meeting_hr_name = []
    data_hr_present = []
    data_hr_absent = []

    meeting_hr_data = HRMeeting.objects.filter(office=met_obj.office)
    for subject in meeting_hr_data:
        attendance_present_count = AttendanceHRReport.objects.filter(meeting=subject.id, status=1,
                                                                     attendant_id=cs_obj.id).count()
        attendance_absent_count = AttendanceHRReport.objects.filter(meeting_id=subject.id, status=1,
                                                                    attendant_id=cs_obj.id).count()
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
        "my_reply": my_reply,
        "all_feedbacks": all_feedbacks,
        "all_unreplied_feedbacks": all_unreplied_feedbacks,
        "all_replied_feedbacks": all_replied_feedbacks,
        "meeting_ceo_name": meeting_ceo_name,
        "data_ceo_present": data_ceo_present,
        "data_ceo_absent": data_ceo_absent,
        "meeting_hr_name": meeting_hr_name,
        "data_hr_present": data_hr_present,
        "data_hr_absent": data_hr_absent
    }
    return render(request, "cs_template/cs_home_template.html", context)


@login_required(login_url='user_login')
def cs_view_ceo_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceCEOReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'cs_template/cs_ceo_attendance.html', context)


@login_required(login_url='user_login')
def cs_view_hr_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceHRReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'cs_template/cs_hr_attendance.html', context)


@login_required(login_url='user_login')
def cs_feedback(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    feedback_data = FeedBackCS.objects.filter(cs_id=cs_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'cs_template/cs_feedback.html', context)


@login_required(login_url='user_login')
def cs_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('cs_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        cs_obj = Customer_service.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackCS(cs_id=cs_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('cs_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('cs_feedback')


@login_required(login_url='user_login')
def feedback_message(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    office = cs_obj.office
    feedbacks = FeedBack.objects.filter(office=office)
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'cs_template/feedback_template.html', context)


@login_required(login_url='user_login')
def my_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    office = cs_obj.office
    feedbacks = FeedBack.objects.filter(office=office, replied_by=cs_obj)
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'cs_template/my_feedback_template.html', context)


@csrf_exempt
def feedback_message_reply(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBack.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.replied_by = cs_obj
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@csrf_exempt
def my_feedback_message_reply(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBack.objects.get(id=feedback_id, replied_by=cs_obj)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def cs_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    leave_data = LeaveReportCS.objects.filter(cs_id=cs_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'cs_template/cs_apply_leave.html', context)


@login_required(login_url='user_login')
def cs_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('cs_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        cs_obj = Customer_service.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportCS(cs_id=cs_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('cs_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('cs_apply_leave')


@login_required(login_url='user_login')
def cs_apply_permission(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    permission_data = PermissionReportCS.objects.filter(cs_id=cs_obj)
    context = {
        "permission_data": permission_data
    }
    return render(request, 'cs_template/cs_apply_permission.html', context)


@login_required(login_url='user_login')
def cs_apply_permission_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('cs_permission_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        cs_obj = Customer_service.objects.get(admin__user=user)
        try:
            leave_report = PermissionReportCS(cs_id=cs_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('cs_apply_permission')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('cs_apply_permission')


@login_required(login_url='user_login')
def cs_profile(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    context={
        "user": user,
        "cs": cs_obj,
    }
    return render(request, 'cs_template/cs_profile.html', context)


@login_required(login_url='user_login')
def cs_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('cs_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.get(id=request.user.id)
            cs_obj = Customer_service.objects.get(admin__user=user)
            customuser = S_CustomUser.objects.get(user=user)
            customuser.user.first_name = first_name
            customuser.user.last_name = last_name
            customuser.user.email = email
            customuser.user.username = username
            if password != None and password != "":
                customuser.user.set_password(password)
            customuser.save()
            cs_obj.address = address
            cs_obj.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('cs_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('cs_profile')


@login_required(login_url='user_login')
def cs_view_notification(request):
    user = User.objects.get(id=request.user.id)
    cs = Customer_service.objects.get(admin__user=user)
    notifications = NotificationCS.objects.filter(cs_id=cs.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "cs_template/cs_view_notification.html", context)


@login_required(login_url='user_login')
def cs_view_def_notification(request):
    user = User.objects.get(id=request.user.id)
    cs = Customer_service.objects.get(admin__user=user)
    def_notifications = DefendantNotificationCS.objects.filter(cs_id=cs.id)
    context = {
        "notifications": def_notifications,
    }
    return render(request, "cs_template/cs_view_def_notification.html", context)


@login_required(login_url='user_login')
def cs_view_acu_notification(request):
    user = User.objects.get(id=request.user.id)
    cs = Customer_service.objects.get(admin__user=user)
    acu_notifications = AccusserNotificationCS.objects.filter(cs_id=cs.id)
    context = {
        "notifications": acu_notifications,
    }
    return render(request, "cs_template/cs_view_acu_notification.html", context)


@login_required(login_url='user_login')
def my_view_cs_resp(request):
    obj = User.objects.get(id=request.user.id)
    user_obj = Customer_service.objects.get(admin__user=obj)
    office = user_obj.office
    resps = ResponsibilityCS.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'cs_template/view_cs_resp.html', context)


@login_required(login_url='user_login')
def cs_feedback_hr(request):
    user = User.objects.get(id=request.user.id)
    cs_obj = Customer_service.objects.get(admin__user=user)
    feedback_data = CSFeedBackHR.objects.filter(cs_id=cs_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'cs_template/cs_feedback_hr.html', context)


@login_required(login_url='user_login')
def cs_feedback_hr_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('cs_feedback_hr')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        cs_obj = Customer_service.objects.get(admin__user=user)

        try:
            add_feedback = CSFeedBackHR(cs_id=cs_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('cs_feedback_hr')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('cs_feedback_hr')
