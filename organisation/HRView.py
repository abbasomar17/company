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
from apartment.models import Drivers
from .forms import *


@login_required(login_url='user_login')
def hr_home(request):
    if Rate.objects.all().exists():
        ob = Rate.objects.all().order_by('created_at')
        obj = ob.first()
        rate = obj.rate / 100
    else:
        rate = 0.07
    hr_salary = 0
    ceo_salary = 0
    swo_salary = 0
    acc_salary = 0
    lawyer_salary = 0
    admin_salary = 0
    overdue_cost = 0
    h_admin_salary = 0
    cs_salary = 0
    a_payment = 0
    h_payment = 0
    o_income = 0
    now = datetime.now()
    year = now.year
    user = User.objects.get(id=request.user.id)
    hr_obj = S_CustomUser.objects.get(user=user)
    met_obj = Human_resource_managers.objects.get(admin=hr_obj)
    office = met_obj.office
    total_ceo_attendance = AttendanceCEOReport.objects.filter(attendant_id=hr_obj).count()
    attendance_ceo_present = AttendanceCEOReport.objects.filter(attendant_id=hr_obj, status=1).count()
    attendance_ceo_absent = AttendanceCEOReport.objects.filter(attendant_id=hr_obj, status=2).count()
    total_hr_attendance = AttendanceHRReport.objects.filter(attendant_id=hr_obj).count()
    attendance_hr_present = AttendanceHRReport.objects.filter(attendant_id=hr_obj, status=1).count()
    attendance_hr_absent = AttendanceHRReport.objects.filter(attendant_id=hr_obj, status=2).count()
    no_ceo_meetings = CEOMeeting.objects.filter(office=office).count()
    no_hr_meetings = HRMeeting.objects.filter(office=office).count()
    no_overdue = Overdue.objects.filter(office=office).count()

    no_office_dis_case = DiscplineMeeting.objects.filter(office=office).count()
    no_office_dis_meeting = DiscplineMeeting.objects.filter(office=office, status=True).count()
    no_all_dis_case = DiscplineMeeting.objects.all().count()
    no_all_dis_meeting = DiscplineMeeting.objects.filter(status=True).count()
    if DiscplineMeeting.objects.all().exists():
        percent_disc_meeting = (no_office_dis_meeting/no_all_dis_meeting) * 100
    else:
        percent_disc_meeting = 0

    if DiscplineMeeting.objects.filter(status=True).exists():
        percent_disc_case = (no_office_dis_case/no_all_dis_case) * 100
    else:
        percent_disc_case = 0

    if DiscplineMeeting.objects.filter(office=office).exists():
        disc_ratio = no_office_dis_meeting/no_office_dis_case
    else:
        disc_ratio = 0

    all_office_count = Office.objects.all().count()
    all_hr_meeting_count = HRMeeting.objects.filter(office=office).count()
    all_hr_count = Human_resource_managers.objects.filter(office=office).count()
    all_swo_count = Social_welfare_officers.objects.filter(office=office).count()
    all_lawyer_count = Lawyers.objects.all().count()
    all_accountant_count = Accountant.objects.filter(office=office).count()
    all_admin_count = AdminHOD.objects.filter(office=office).count()
    all_h_admin_count = H_AdminHOD.objects.filter(office=office).count()
    all_cs_count = Customer_service.objects.filter(office=office).count()
    all_ceo_count = CEO.objects.filter(office=office).count()
    total_staff = all_cs_count + all_h_admin_count + all_admin_count + all_hr_count + all_lawyer_count + all_accountant_count + all_swo_count + all_ceo_count

    if CEO.objects.filter(office=office).exists():
        all_ceo_accept_leave_count = LeaveReportCEO.objects.filter(ceo_id__office=office, leave_status=1).count()
    else:
        all_ceo_accept_leave_count = 0
    if Human_resource_managers.objects.filter(office=office).exists():
        all_hr_accept_leave_count = LeaveReportHR.objects.filter(hr_id__office=office, leave_status=1).count()
    else:
        all_hr_accept_leave_count = 0
    if Social_welfare_officers.objects.filter(office=office).exists():
        all_swo_accept_leave_count = LeaveReportSWO.objects.filter(swo_id__office=office, leave_status=1).count()
    else:
        all_swo_accept_leave_count = 0
    if Lawyers.objects.all().exists():
        all_lawyer_accept_leave_count = LeaveReportLawyer.objects.filter(leave_status=1).count()
    else:
        all_lawyer_accept_leave_count = 0
    if Accountant.objects.filter(office=office).exists():
        all_accountant_accept_leave_count = LeaveReportAccountant.objects.filter(accountant_id__office=office, leave_status=1).count()
    else:
        all_accountant_accept_leave_count = 0
    if AdminHOD.objects.filter(office=office).exists():
        all_admin_accept_leave_count = LeaveReportAdmin.objects.filter(admin_id__office=office, leave_status=1).count()
    else:
        all_admin_accept_leave_count = 0
    if H_AdminHOD.objects.filter(office=office).exists():
        all_h_admin_accept_leave_count = LeaveReportH_Admin.objects.filter(h_admin_id__office=office, leave_status=1).count()
    else:
        all_h_admin_accept_leave_count = 0
    if Customer_service.objects.filter(office=office).exists():
        all_cs_accept_leave_count = LeaveReportCS.objects.filter(cs_id__office=office, leave_status=1).count()
    else:
        all_cs_accept_leave_count = 0

    total_accept_leave = all_ceo_accept_leave_count + all_cs_accept_leave_count + all_h_admin_accept_leave_count + all_admin_accept_leave_count + all_lawyer_accept_leave_count + all_accountant_accept_leave_count + all_swo_accept_leave_count + all_hr_accept_leave_count

    if CEO.objects.filter(office=office).exists():
        all_ceo_reject_leave_count = LeaveReportCEO.objects.filter(ceo_id__office=office, leave_status=2).count()
    else:
        all_ceo_reject_leave_count = 0
    if Human_resource_managers.objects.filter(office=office).exists():
        all_hr_reject_leave_count = LeaveReportHR.objects.filter(hr_id__office=office, leave_status=2).count()
    else:
        all_hr_reject_leave_count = 0
    if Social_welfare_officers.objects.filter(office=office).exists():
        all_swo_reject_leave_count = LeaveReportSWO.objects.filter(swo_id__office=office, leave_status=2).count()
    else:
        all_swo_reject_leave_count = 0
    if Lawyers.objects.all().exists():
        all_lawyer_reject_leave_count = LeaveReportLawyer.objects.filter(leave_status=2).count()
    else:
        all_lawyer_reject_leave_count = 0
    if Accountant.objects.filter(office=office).exists():
        all_accountant_reject_leave_count = LeaveReportAccountant.objects.filter(accountant_id__office=office,
                                                                                 leave_status=2).count()
    else:
        all_accountant_reject_leave_count = 0
    if AdminHOD.objects.filter(office=office).exists():
        all_admin_reject_leave_count = LeaveReportAdmin.objects.filter(admin_id__office=office, leave_status=2).count()
    else:
        all_admin_reject_leave_count = 0
    if H_AdminHOD.objects.filter(office=office).exists():
        all_h_admin_reject_leave_count = LeaveReportH_Admin.objects.filter(h_admin_id__office=office,
                                                                           leave_status=2).count()
    else:
        all_h_admin_reject_leave_count = 0
    if Customer_service.objects.filter(office=office).exists():
        all_cs_reject_leave_count = LeaveReportCS.objects.filter(cs_id__office=office, leave_status=2).count()
    else:
        all_cs_reject_leave_count = 0

    total_reject_leave = all_ceo_reject_leave_count + all_cs_reject_leave_count + all_h_admin_reject_leave_count + all_admin_reject_leave_count + all_lawyer_reject_leave_count + all_accountant_reject_leave_count + all_swo_reject_leave_count + all_hr_reject_leave_count

    if CEO.objects.filter(office=office).exists():
        all_ceo_pending_leave_count = LeaveReportCEO.objects.filter(ceo_id__office=office, leave_status=0).count()
    else:
        all_ceo_pending_leave_count = 0
    if Human_resource_managers.objects.filter(office=office).exists():
        all_hr_pending_leave_count = LeaveReportHR.objects.filter(hr_id__office=office, leave_status=0).count()
    else:
        all_hr_pending_leave_count = 0
    if Social_welfare_officers.objects.filter(office=office).exists():
        all_swo_pending_leave_count = LeaveReportSWO.objects.filter(swo_id__office=office, leave_status=0).count()
    else:
        all_swo_pending_leave_count = 0
    if Lawyers.objects.all().exists():
        all_lawyer_pending_leave_count = LeaveReportLawyer.objects.filter(leave_status=0).count()
    else:
        all_lawyer_pending_leave_count = 0
    if Accountant.objects.filter(office=office).exists():
        all_accountant_pending_leave_count = LeaveReportAccountant.objects.filter(accountant_id__office=office,
                                                                                  leave_status=0).count()
    else:
        all_accountant_pending_leave_count = 0
    if AdminHOD.objects.filter(office=office).exists():
        all_admin_pending_leave_count = LeaveReportAdmin.objects.filter(admin_id__office=office, leave_status=0).count()
    else:
        all_admin_pending_leave_count = 0
    if H_AdminHOD.objects.filter(office=office).exists():
        all_h_admin_pending_leave_count = LeaveReportH_Admin.objects.filter(h_admin_id__office=office,
                                                                            leave_status=0).count()
    else:
        all_h_admin_pending_leave_count = 0
    if Customer_service.objects.filter(office=office).exists():
        all_cs_pending_leave_count = LeaveReportCS.objects.filter(cs_id__office=office, leave_status=0).count()
    else:
        all_cs_pending_leave_count = 0

    total_pending_leave = all_ceo_pending_leave_count + all_cs_pending_leave_count + all_h_admin_pending_leave_count + all_admin_pending_leave_count + all_lawyer_pending_leave_count + all_accountant_pending_leave_count + all_swo_pending_leave_count + all_hr_pending_leave_count

    total_leaves = total_reject_leave + total_pending_leave + total_accept_leave

    if total_leaves != 0:
        percent_accept_leaves = (total_accept_leave/total_leaves) * 100
        percent_reject_leaves = (total_reject_leave / total_leaves) * 100
        percent_pending_leaves = (total_pending_leave / total_leaves) * 100
    else:
        percent_accept_leaves = 0
        percent_reject_leaves = 0
        percent_pending_leaves = 0

    if CEO.objects.filter(office=office).exists():
        all_ceo_accept_perm_count = PermissionReportCEO.objects.filter(ceo_id__office=office, leave_status=1).count()
    else:
        all_ceo_accept_perm_count = 0
    if Human_resource_managers.objects.filter(office=office).exists():
        all_hr_accept_perm_count = PermissionReportHR.objects.filter(hr_id__office=office, leave_status=1).count()
    else:
        all_hr_accept_perm_count = 0
    if Social_welfare_officers.objects.filter(office=office).exists():
        all_swo_accept_perm_count = PermissionReportSWO.objects.filter(swo_id__office=office, leave_status=1).count()
    else:
        all_swo_accept_perm_count = 0
    if Lawyers.objects.all().exists():
        all_lawyer_accept_perm_count = PermissionReportLawyer.objects.filter(leave_status=1).count()
    else:
        all_lawyer_accept_perm_count = 0
    if Accountant.objects.filter(office=office).exists():
        all_accountant_accept_perm_count = PermissionReportAccountant.objects.filter(accountant_id__office=office,
                                                                                     leave_status=1).count()
    else:
        all_accountant_accept_perm_count = 0
    if AdminHOD.objects.filter(office=office).exists():
        all_admin_accept_perm_count = PermissionReportAdmin.objects.filter(admin_id__office=office,
                                                                           leave_status=1).count()
    else:
        all_admin_accept_perm_count = 0
    if H_AdminHOD.objects.filter(office=office).exists():
        all_h_admin_accept_perm_count = PermissionReportH_Admin.objects.filter(h_admin_id__office=office,
                                                                               leave_status=1).count()
    else:
        all_h_admin_accept_perm_count = 0
    if Customer_service.objects.filter(office=office).exists():
        all_cs_accept_perm_count = PermissionReportCS.objects.filter(cs_id__office=office, leave_status=1).count()
    else:
        all_cs_accept_perm_count = 0

    total_accept_perm = all_ceo_accept_perm_count + all_cs_accept_perm_count + all_h_admin_accept_perm_count + all_admin_accept_perm_count + all_lawyer_accept_perm_count + all_accountant_accept_perm_count + all_swo_accept_perm_count + all_hr_accept_perm_count

    if CEO.objects.filter(office=office).exists():
        all_ceo_reject_perm_count = PermissionReportCEO.objects.filter(ceo_id__office=office, leave_status=2).count()
    else:
        all_ceo_reject_perm_count = 0
    if Human_resource_managers.objects.filter(office=office).exists():
        all_hr_reject_perm_count = PermissionReportHR.objects.filter(hr_id__office=office, leave_status=2).count()
    else:
        all_hr_reject_perm_count = 0
    if Social_welfare_officers.objects.filter(office=office).exists():
        all_swo_reject_perm_count = PermissionReportSWO.objects.filter(swo_id__office=office, leave_status=2).count()
    else:
        all_swo_reject_perm_count = 0
    if Lawyers.objects.all().exists():
        all_lawyer_reject_perm_count = PermissionReportLawyer.objects.filter(leave_status=2).count()
    else:
        all_lawyer_reject_perm_count = 0
    if Accountant.objects.filter(office=office).exists():
        all_accountant_reject_perm_count = PermissionReportAccountant.objects.filter(accountant_id__office=office,
                                                                                     leave_status=2).count()
    else:
        all_accountant_reject_perm_count = 0
    if AdminHOD.objects.filter(office=office).exists():
        all_admin_reject_perm_count = PermissionReportAdmin.objects.filter(admin_id__office=office,
                                                                           leave_status=2).count()
    else:
        all_admin_reject_perm_count = 0
    if H_AdminHOD.objects.filter(office=office).exists():
        all_h_admin_reject_perm_count = PermissionReportH_Admin.objects.filter(h_admin_id__office=office,
                                                                               leave_status=2).count()
    else:
        all_h_admin_reject_perm_count = 0
    if Customer_service.objects.filter(office=office).exists():
        all_cs_reject_perm_count = PermissionReportCS.objects.filter(cs_id__office=office, leave_status=2).count()
    else:
        all_cs_reject_perm_count = 0

    total_reject_perm = all_ceo_reject_perm_count + all_cs_reject_perm_count + all_h_admin_reject_perm_count + all_admin_reject_perm_count + all_lawyer_reject_perm_count + all_accountant_reject_perm_count + all_swo_reject_perm_count + all_hr_reject_perm_count

    if CEO.objects.filter(office=office).exists():
        all_ceo_pending_perm_count = PermissionReportCEO.objects.filter(ceo_id__office=office, leave_status=0).count()
    else:
        all_ceo_pending_perm_count = 0
    if Human_resource_managers.objects.filter(office=office).exists():
        all_hr_pending_perm_count = PermissionReportHR.objects.filter(hr_id__office=office, leave_status=0).count()
    else:
        all_hr_pending_perm_count = 0
    if Social_welfare_officers.objects.filter(office=office).exists():
        all_swo_pending_perm_count = PermissionReportSWO.objects.filter(swo_id__office=office, leave_status=0).count()
    else:
        all_swo_pending_perm_count = 0
    if Lawyers.objects.all().exists():
        all_lawyer_pending_perm_count = PermissionReportLawyer.objects.filter(leave_status=0).count()
    else:
        all_lawyer_pending_perm_count = 0
    if Accountant.objects.filter(office=office).exists():
        all_accountant_pending_perm_count = PermissionReportAccountant.objects.filter(accountant_id__office=office,
                                                                                      leave_status=0).count()
    else:
        all_accountant_pending_perm_count = 0
    if AdminHOD.objects.filter(office=office).exists():
        all_admin_pending_perm_count = PermissionReportAdmin.objects.filter(admin_id__office=office,
                                                                            leave_status=0).count()
    else:
        all_admin_pending_perm_count = 0
    if H_AdminHOD.objects.filter(office=office).exists():
        all_h_admin_pending_perm_count = PermissionReportH_Admin.objects.filter(h_admin_id__office=office,
                                                                                leave_status=0).count()
    else:
        all_h_admin_pending_perm_count = 0
    if Customer_service.objects.filter(office=office).exists():
        all_cs_pending_perm_count = PermissionReportCS.objects.filter(cs_id__office=office, leave_status=0).count()
    else:
        all_cs_pending_perm_count = 0

    total_pending_perm = all_ceo_pending_perm_count + all_cs_pending_perm_count + all_h_admin_pending_perm_count + all_admin_pending_perm_count + all_lawyer_pending_perm_count + all_accountant_pending_perm_count + all_swo_pending_perm_count + all_hr_pending_perm_count

    total_perms = total_reject_perm + total_pending_perm + total_accept_perm

    if total_perms != 0:
        percent_accept_perms = (total_accept_perm / total_perms) * 100
        percent_reject_perms = (total_reject_perm / total_perms) * 100
        percent_pending_perms = (total_pending_perm / total_perms) * 100
    else:
        percent_accept_perms = 0
        percent_reject_perms = 0
        percent_pending_perms = 0

    if SalaryLawyer.objects.all().exists() and Lawyers.objects.all().exists():
        all_lawyers = Lawyers.objects.all()
        for lawyer in all_lawyers:
            employed = lawyer.created_at.year
            t = int((year - employed) / 3)
            no_salary = SalaryLawyer.objects.all().first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            lawyer_salary = round((lawyer_salary + new_salary), 2)
        law_sal_year = lawyer_salary * 12
    else:
        law_sal_year = 0

    if SalaryCEO.objects.filter(office=office).exists() and CEO.objects.filter(office=office).exists():
        office_ceo = CEO.objects.get(office=office)
        employed = office_ceo.created_at.year
        t = int((year - employed) / 3)
        no_salary = SalaryCEO.objects.filter(office=office).first()
        new_salary = no_salary.amount * (pow((1 + rate), t))
        ceo_salary = round((ceo_salary + new_salary), 2)
        ceo_sal_year = ceo_salary * 12
    else:
        ceo_sal_year = 0

    if SalaryHR.objects.filter(office=office).exists() and Human_resource_managers.objects.filter(
            office=office).exists():
        office_hrs = Human_resource_managers.objects.filter(office=office)
        for hr in office_hrs:
            employed = hr.created_at.year
            t = int((year - employed) / 3)
            no_salary = SalaryHR.objects.filter(office=office).first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            hr_salary = round((hr_salary + new_salary), 2)
        hr_sal_year = hr_salary * 12
    else:
        hr_sal_year = 0

    if SalarySWO.objects.filter(office=office).exists() and Social_welfare_officers.objects.filter(
            office=office).exists():
        office_swos = Social_welfare_officers.objects.filter(office=office)
        for swo in office_swos:
            employed = swo.created_at.year
            t = (year - employed) / 3
            no_salary = SalarySWO.objects.filter(office=office).first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            swo_salary = swo_salary + new_salary
        swo_sal_year = swo_salary * 12
    else:
        swo_sal_year = 0

    if SalaryAccountant.objects.filter(office=office).exists() and Accountant.objects.filter(office=office).exists():
        office_accs = Accountant.objects.filter(office=office)
        for acc in office_accs:
            employed = acc.created_at.year
            t = int((year - employed) / 3)
            no_salary = SalaryAccountant.objects.filter(office=office).first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            acc_salary = round((acc_salary + new_salary), 2)
        acc_sal_year = acc_salary * 12
    else:
        acc_sal_year = 0

    if SalaryAdmin.objects.filter(office=office).exists() and H_AdminHOD.objects.filter(office=office).exists():
        office_h_admin = H_AdminHOD.objects.filter(office=office)
        for h_admin in office_h_admin:
            employed = h_admin.created_at.year
            t = int((year - employed) / 3)
            no_salary = SalaryAdmin.objects.filter(office=office).first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            h_admin_salary = round((h_admin_salary + new_salary), 2)
        h_admin_sal_year = h_admin_salary * 12
    else:
        h_admin_sal_year = 0

    if SalaryAdmin.objects.filter(office=office).exists() and AdminHOD.objects.filter(office=office).exists():
        office_admin = AdminHOD.objects.filter(office=office)
        for admin in office_admin:
            employed = admin.created_at.year
            t = int((year - employed) / 3)
            no_salary = SalaryAdmin.objects.filter(office=office).first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            admin_salary = round((admin_salary + new_salary), 2)
        admin_sal_year = admin_salary * 12
    else:
        admin_sal_year = 0

    if SalaryCS.objects.filter(office=office).exists() and Customer_service.objects.filter(office=office).exists():
        office_css = Customer_service.objects.filter(office=office)
        for cs in office_css:
            employed = cs.created_at.year
            t = int((year - employed) / 3)
            no_salary = SalaryCS.objects.filter(office=office).first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            cs_salary = round((cs_salary + new_salary), 2)
        cs_sal_year = cs_salary * 12
    else:
        cs_sal_year = 0

    if Office.objects.all().exists():
        office_law_sal = law_sal_year / all_office_count
    else:
        office_law_sal = 0

    total_salary = ceo_sal_year + cs_sal_year + admin_sal_year + h_admin_sal_year + office_law_sal + hr_sal_year + acc_sal_year + swo_sal_year


    all_overdue = Overdue.objects.filter(office=office)
    for overdue in all_overdue:
        amount = overdue.amount
        overdue_cost = overdue_cost + amount

    total_expenditure = total_salary + overdue_cost

    all_a_p = ApartmentPayment.objects.filter(office=office)
    for a_p in all_a_p:
        amount = a_p.amount
        a_payment = a_payment + amount

    all_income = Incomes.objects.filter(office=office)
    for income in all_income:
        amount = income.amount
        o_income = o_income + amount

    total_income = h_payment + o_income + a_payment

    meeting_ceo_all = CEOMeeting.objects.filter(office=office)
    meeting_ceo_name_list = []
    topics_ceo_count_list = []

    for meeting in meeting_ceo_all:
        topics = CEOTopics.objects.filter(meeting_id=meeting.id).count()
        meeting_ceo_name_list.append(meeting.meeting_name)
        topics_ceo_count_list.append(topics)

    meeting_hr_all = HRMeeting.objects.filter(office=office)
    meeting_hr_name_list = []
    topics_hr_count_list = []

    for meeting in meeting_hr_all:
        topics = HRTopics.objects.filter(meeting_id=meeting.id).count()
        meeting_hr_name_list.append(meeting.meeting_name)
        topics_hr_count_list.append(topics)

    meeting_ceo_name = []
    data_ceo_present = []
    data_ceo_absent = []
    meeting_ceo_data = CEOMeeting.objects.filter(office=office)
    for subject in meeting_ceo_data:
        attendance_present_count = AttendanceCEOReport.objects.filter(meeting_id=subject.id, status=1,
                                                                      attendant_id=hr_obj.id).count()
        attendance_absent_count = AttendanceCEOReport.objects.filter(meeting=subject.id, status=2,
                                                                     attendant_id=hr_obj.id).count()
        meeting_ceo_name.append(subject.meeting_name)
        data_ceo_present.append(attendance_present_count)
        data_ceo_absent.append(attendance_absent_count)

    meeting_hr_name = []
    data_hr_present = []
    data_hr_absent = []

    meeting_hr_data = HRMeeting.objects.filter(office=office)
    for subject in meeting_hr_data:
        attendance_present_count = AttendanceHRReport.objects.filter(meeting=subject.id, status=1,
                                                                     attendant_id=hr_obj.id).count()
        attendance_absent_count = AttendanceHRReport.objects.filter(meeting_id=subject.id, status=1,
                                                                    attendant_id=hr_obj.id).count()
        meeting_hr_name.append(subject.meeting_name)
        data_hr_present.append(attendance_present_count)
        data_hr_absent.append(attendance_absent_count)

    context = {
        "total_staff": total_staff,
        "rate": rate,
        "hr_salary": hr_sal_year,
        "ceo_salary": ceo_sal_year,
        "swo_salary": swo_sal_year,
        "acc_salary": acc_sal_year,
        "lawyer_salary": law_sal_year,
        "office_law_sal": office_law_sal,
        "admin_salary": admin_sal_year,
        "overdue_cost": overdue_cost,
        "h_admin_salary": h_admin_sal_year,
        "cs_salary": cs_sal_year,
        "a_payment": a_payment,
        "h_payment": h_payment,
        "o_income": o_income,
        "total_salary": total_salary,
        "total_expenditure": total_expenditure,
        "total_income": total_income,
        "total_hr_attendance": total_hr_attendance,
        "attendance_hr_present": attendance_hr_present,
        "attendance_hr_absent": attendance_hr_absent,
        "total_ceo_attendance": total_ceo_attendance,
        "attendance_ceo_present": attendance_ceo_present,
        "attendance_ceo_absent": attendance_ceo_absent,
        "meeting_ceo_name": meeting_ceo_name,
        "data_ceo_present": data_ceo_present,
        "data_ceo_absent": data_ceo_absent,
        "meeting_hr_name": meeting_hr_name,
        "data_hr_present": data_hr_present,
        "data_hr_absent": data_hr_absent,
        "no_hr_meetings": no_hr_meetings,
        "no_ceo_meetings": no_ceo_meetings,
        "no_overdue": no_overdue,
        "meeting_ceo_name_list": meeting_ceo_name_list,
        "topics_ceo_count_list": topics_ceo_count_list,
        "meeting_hr_name_list": meeting_hr_name_list,
        "topics_hr_count_list": topics_hr_count_list,
        "all_cs_count": all_cs_count,
        "all_ceo_count": all_ceo_count,
        "all_h_admin_count": all_h_admin_count,
        "all_admin_count": all_admin_count,
        "all_accountant_count": all_accountant_count,
        "all_office_count": all_office_count,
        "all_lawyer_count": all_lawyer_count,
        "all_hr_meeting_count": all_hr_meeting_count,
        "all_swo_count": all_swo_count,
        "all_hr_count": all_hr_count,
        "no_office_dis_case": no_office_dis_case,
        "no_office_dis_meeting": no_office_dis_meeting,
        "no_all_dis_case": no_all_dis_case,
        "no_all_dis_meeting": no_all_dis_meeting,
        "percent_disc_meeting": percent_disc_meeting,
        "percent_disc_case": percent_disc_case,
        "disc_ratio": disc_ratio,
        "all_ceo_accept_leave_count": all_ceo_accept_leave_count,
        "all_hr_accept_leave_count": all_hr_accept_leave_count,
        "all_swo_accept_leave_count": all_swo_accept_leave_count,
        "all_lawyer_accept_leave_count": all_lawyer_accept_leave_count,
        "all_accountant_accept_leave_count": all_accountant_accept_leave_count,
        "all_admin_accept_leave_count": all_admin_accept_leave_count,
        "all_h_admin_accept_leave_count": all_h_admin_accept_leave_count,
        "all_cs_accept_leave_count": all_cs_accept_leave_count,
        "total_accept_leave": total_accept_leave,
        "all_ceo_reject_leave_count": all_ceo_reject_leave_count,
        "all_hr_reject_leave_count": all_hr_reject_leave_count,
        "all_swo_reject_leave_count": all_swo_reject_leave_count,
        "all_lawyer_reject_leave_count": all_lawyer_reject_leave_count,
        "all_accountant_reject_leave_count": all_accountant_reject_leave_count,
        "all_admin_reject_leave_count": all_admin_reject_leave_count,
        "all_h_admin_reject_leave_count": all_h_admin_reject_leave_count,
        "all_cs_reject_leave_count": all_cs_reject_leave_count,
        "total_reject_leave": total_reject_leave,
        "all_ceo_pending_leave_count": all_ceo_pending_leave_count,
        "all_hr_pending_leave_count": all_hr_pending_leave_count,
        "all_swo_pending_leave_count": all_swo_pending_leave_count,
        "all_lawyer_pending_leave_count": all_lawyer_pending_leave_count,
        "all_accountant_pending_leave_count": all_accountant_pending_leave_count,
        "all_admin_pending_leave_count": all_admin_pending_leave_count,
        "all_h_admin_pending_leave_count": all_h_admin_pending_leave_count,
        "all_cs_pending_leave_count": all_cs_pending_leave_count,
        "total_pending_leave": total_pending_leave,
        "total_leaves": total_leaves,
        "percent_accept_leaves": percent_accept_leaves,
        "percent_reject_leaves": percent_reject_leaves,
        "percent_pending_leaves": percent_pending_leaves,
        "all_ceo_accept_perm_count": all_ceo_accept_perm_count,
        "all_hr_accept_perm_count": all_hr_accept_perm_count,
        "all_swo_accept_perm_count": all_swo_accept_perm_count,
        "all_lawyer_accept_perm_count": all_lawyer_accept_perm_count,
        "all_accountant_accept_perm_count": all_accountant_accept_perm_count,
        "all_admin_accept_perm_count": all_admin_accept_perm_count,
        "all_h_admin_accept_perm_count": all_h_admin_accept_perm_count,
        "all_cs_accept_perm_count": all_cs_accept_perm_count,
        "total_accept_perm": total_accept_perm,
        "all_ceo_reject_perm_count": all_ceo_reject_perm_count,
        "all_hr_reject_perm_count": all_hr_reject_perm_count,
        "all_swo_reject_perm_count": all_swo_reject_perm_count,
        "all_lawyer_reject_perm_count": all_lawyer_reject_perm_count,
        "all_accountant_reject_perm_count": all_accountant_reject_perm_count,
        "all_admin_reject_perm_count": all_admin_reject_perm_count,
        "all_h_admin_reject_perm_count": all_h_admin_reject_perm_count,
        "all_cs_reject_perm_count": all_cs_reject_perm_count,
        "total_reject_perm": total_reject_perm,
        "all_ceo_pending_perm_count": all_ceo_pending_perm_count,
        "all_hr_pending_perm_count": all_hr_pending_perm_count,
        "all_swo_pending_perm_count": all_swo_pending_perm_count,
        "all_lawyer_pending_perm_count": all_lawyer_pending_perm_count,
        "all_accountant_pending_perm_count": all_accountant_pending_perm_count,
        "all_admin_pending_perm_count": all_admin_pending_perm_count,
        "all_h_admin_pending_perm_count": all_h_admin_pending_perm_count,
        "all_cs_pending_perm_count": all_cs_pending_perm_count,
        "total_pending_perm": total_pending_perm,
        "total_perms": total_perms,
        "percent_accept_perms": percent_accept_perms,
        "percent_reject_perms": percent_reject_perms,
        "percent_pending_perms": percent_pending_perms,
    }
    return render(request, "hr_template/hr_home_template.html", context)


@login_required(login_url='user_login')
def hr_view_ceo_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceCEOReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'hr_template/hr_ceo_attendance.html', context)


@login_required(login_url='user_login')
def hr_view_hr_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceHRReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'hr_template/hr_hr_attendance.html', context)


@login_required(login_url='user_login')
def add_law(request):
    form = AddLawyerForm()
    context = {
        "form": form
    }
    return render(request, 'hr_template/add_law_template.html', context)


@login_required(login_url='user_login')
def add_law_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        law_form = AddLawyerForm(request.POST)
        if customer_form.is_valid() and law_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = law_form.cleaned_data['address']
            nida_number = law_form.cleaned_data['nida_number']

            obj = User.objects.get(id=request.user.id)
            hr_obj = Human_resource_managers.objects.get(admin__user=obj)
            office_obj = hr_obj.office

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type = 4)
            customer.save()


            law = Lawyers(admin=customer, address=address, nida_number=nida_number)
            law.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_law')
    else:
        customer_form = AddCustomerForm()
        law_form = AddLawyerForm()
        context = {
            'customer_form': customer_form,
            'law_form': law_form
        }
        return render(request, 'hr_template/add_law_template.html', context)


@login_required(login_url='user_login')
def manage_law(request):
    laws = Lawyers.objects.all()
    context = {
        "laws": laws
    }
    return render(request, 'hr_template/manage_law_template.html', context)


@login_required(login_url='user_login')
def edit_law(request, law_id):
    # Adding Student ID into Session Variable
    request.session['law_id'] = law_id

    law = Lawyers.objects.get(admin=law_id)
    form = EditLawyerForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = law.admin.user.email
    form.fields['username'].initial = law.admin.user.username
    form.fields['first_name'].initial = law.admin.user.first_name
    form.fields['last_name'].initial = law.admin.user.last_name
    form.fields['address'].initial = law.address


    context = {
        "id": law_id,
        "username": law.admin.user.username,
        "form": form
    }
    return render(request, "hr_template/edit_law_template.html", context)


@login_required(login_url='user_login')
def edit_law_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        law_id = request.session.get('law_id')
        if law_id == None:
            return redirect('manage_law')

        form = EditLawyerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']

            try:
                # First Update into Custom User Model
                user = Lawyers.objects.get(id=law_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username


                # Then Update Students Table

                user.address = address

                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['law_id']

                messages.success(request, "Staff Updated Successfully!")
                return redirect('/edit_law/'+law_id)
            except:
                messages.success(request, "Failed to Update Staff.")
                return redirect('/edit_law/'+law_id)
        else:
            return redirect('/edit_law/'+law_id)


@login_required(login_url='user_login')
def delete_law(request, law_id):
    law = Lawyers.objects.get(id=law_id)
    try:
        law.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_law')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_law')


@login_required(login_url='user_login')
def add_swo(request):
    form = AddSWOForm()
    context = {
        "form": form
    }
    return render(request, 'hr_template/add_swo_template.html', context)


@login_required(login_url='user_login')
def add_swo_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        swo_form = AddSWOForm(request.POST)
        if customer_form.is_valid() and swo_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = swo_form.cleaned_data['address']
            nida_number = swo_form.cleaned_data['nida_number']

            obj = User.objects.get(id=request.user.id)
            hr_obj = Human_resource_managers.objects.get(admin__user=obj)
            office_obj = hr_obj.office

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type = 3)
            customer.save()


            staff = Social_welfare_officers(admin=customer, address=address, office=office_obj, nida_number=nida_number)
            staff.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_swo')
    else:
        customer_form = AddCustomerForm()
        swo_form = AddSWOForm()
        context = {
            'customer_form': customer_form,
            'swo_form': swo_form
        }
        return render(request, 'hr_template/add_swo_template.html', context)


@login_required(login_url='user_login')
def manage_swo(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office_obj = hr_obj.office
    swos = Social_welfare_officers.objects.filter(office=office_obj)
    context = {
        "swos": swos
    }
    return render(request, 'hr_template/manage_swo_template.html', context)


@login_required(login_url='user_login')
def edit_swo(request, swo_id):
    # Adding Student ID into Session Variable
    request.session['swo_id'] = swo_id

    swo = Social_welfare_officers.objects.get(admin=swo_id)
    form = EditSWOForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = swo.admin.user.email
    form.fields['username'].initial = swo.admin.user.username
    form.fields['first_name'].initial = swo.admin.user.first_name
    form.fields['last_name'].initial = swo.admin.user.last_name
    form.fields['address'].initial = swo.address


    context = {
        "id": swo_id,
        "username": swo.admin.user.username,
        "form": form
    }
    return render(request, "hr_template/edit_swo_template.html", context)


@login_required(login_url='user_login')
def edit_swo_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        swo_id = request.session.get('swo_id')
        if swo_id == None:
            return redirect('manage_swo')

        form = EditSWOForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']

            try:
                # First Update into Custom User Model
                user = Social_welfare_officers.objects.get(id=swo_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username


                # Then Update Students Table

                user.address = address

                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['swo_id']

                messages.success(request, "Staff Updated Successfully!")
                return redirect('/edit_swo/'+swo_id)
            except:
                messages.success(request, "Failed to Update Staff.")
                return redirect('/edit_swo/'+swo_id)
        else:
            return redirect('/edit_swo/'+swo_id)


@login_required(login_url='user_login')
def delete_swo(request, swo_id):
    swo = Social_welfare_officers.objects.get(id=swo_id)
    try:
        swo.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_swo')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_swo')


@login_required(login_url='user_login')
def add_cs(request):
    form = AddCSForm()
    context = {
        "form": form
    }
    return render(request, 'hr_template/add_cs_template.html', context)


@login_required(login_url='user_login')
def add_cs_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        cs_form = AddCSForm(request.POST)
        if customer_form.is_valid() and cs_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = cs_form.cleaned_data['address']
            nida_number = cs_form.cleaned_data['nida_number']

            obj = User.objects.get(id=request.user.id)
            hr_obj = Human_resource_managers.objects.get(admin__user=obj)
            office_obj = hr_obj.office

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type=5)
            customer.save()

            staff = Customer_service(admin=customer, address=address, office=office_obj, nida_number=nida_number)
            staff.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_cs')
    else:
        customer_form = AddCustomerForm()
        cs_form = AddCSForm()
        context = {
            'customer_form': customer_form,
            'cs_form': cs_form
        }
        return render(request, 'hr_template/add_cs_template.html', context)


@login_required(login_url='user_login')
def manage_cs(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office_obj = hr_obj.office
    css = Customer_service.objects.filter(office=office_obj)
    context = {
        "css": css
    }
    return render(request, 'hr_template/manage_cs_template.html', context)


@login_required(login_url='user_login')
def edit_cs(request, cs_id):
    # Adding Student ID into Session Variable
    request.session['cs_id'] = cs_id

    cs = Customer_service.objects.get(admin=cs_id)
    form = EditCSForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = cs.admin.user.email
    form.fields['username'].initial = cs.admin.user.username
    form.fields['first_name'].initial = cs.admin.user.first_name
    form.fields['last_name'].initial = cs.admin.user.last_name
    form.fields['address'].initial = cs.address

    context = {
        "id": cs_id,
        "username": cs.admin.user.username,
        "form": form
    }
    return render(request, "hr_template/edit_cs_template.html", context)


@login_required(login_url='user_login')
def edit_cs_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        cs_id = request.session.get('cs_id')
        if cs_id == None:
            return redirect('manage_cs')

        form = EditCSForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']

            try:
                # First Update into Custom User Model
                user = Customer_service.objects.get(id=cs_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username

                # Then Update Students Table

                user.address = address

                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['cs_id']

                messages.success(request, "Staff Updated Successfully!")
                return redirect('/edit_cs/' + cs_id)
            except:
                messages.success(request, "Failed to Update Staff.")
                return redirect('/edit_cs/' + cs_id)
        else:
            return redirect('/edit_cs/' + cs_id)


@login_required(login_url='user_login')
def delete_cs(request, cs_id):
    cs = Customer_service.objects.get(id=cs_id)
    try:
        cs.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_cs')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_cs')


@login_required(login_url='user_login')
def add_acc(request):
    form = AddAccountantForm()
    context = {
        "form": form
    }
    return render(request, 'hr_template/add_acc_template.html', context)


@login_required(login_url='user_login')
def add_acc_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        acc_form = AddAccountantForm(request.POST)
        if customer_form.is_valid() and acc_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = acc_form.cleaned_data['address']
            nida_number = acc_form.cleaned_data['nida_number']

            obj = User.objects.get(id=request.user.id)
            hr_obj = Human_resource_managers.objects.get(admin__user=obj)
            office_obj = hr_obj.office

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type=6)
            customer.save()

            staff = Accountant(admin=customer, address=address, office=office_obj, nida_number=nida_number)
            staff.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_acc')
    else:
        customer_form = AddCustomerForm()
        acc_form = AddAccountantForm()
        context = {
            'customer_form': customer_form,
            'acc_form': acc_form
        }
        return render(request, 'hr_template/add_acc_template.html', context)


@login_required(login_url='user_login')
def manage_acc(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office_obj = hr_obj.office
    accs = Accountant.objects.filter(office=office_obj)
    context = {
        "accs": accs
    }
    return render(request, 'hr_template/manage_acc_template.html', context)


@login_required(login_url='user_login')
def edit_acc(request, acc_id):
    # Adding Student ID into Session Variable
    request.session['acc_id'] = acc_id

    acc = Accountant.objects.get(admin=acc_id)
    form = EditAccountantForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = acc.admin.user.email
    form.fields['username'].initial = acc.admin.user.username
    form.fields['first_name'].initial = acc.admin.user.first_name
    form.fields['last_name'].initial = acc.admin.user.last_name
    form.fields['address'].initial = acc.address

    context = {
        "id": acc_id,
        "username": acc.admin.user.username,
        "form": form
    }
    return render(request, "hr_template/edit_acc_template.html", context)


@login_required(login_url='user_login')
def edit_acc_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        acc_id = request.session.get('acc_id')
        if acc_id == None:
            return redirect('manage_acc')

        form = EditAccountantForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']

            try:
                # First Update into Custom User Model
                user = Accountant.objects.get(id=acc_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username

                # Then Update Students Table

                user.address = address

                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['acc_id']

                messages.success(request, "Staff Updated Successfully!")
                return redirect('/edit_acc/' + acc_id)
            except:
                messages.success(request, "Failed to Update Staff.")
                return redirect('/edit_acc/' + acc_id)
        else:
            return redirect('/edit_acc/' + acc_id)


@login_required(login_url='user_login')
def delete_acc(request, acc_id):
    acc = Accountant.objects.get(id=acc_id)
    try:
        acc.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_acc')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_acc')


@login_required(login_url='user_login')
def add_h_admin(request):
    form = AddSWOForm()
    context = {
        "form": form
    }
    return render(request, 'hr_template/add_h_admin_template.html', context)


@login_required(login_url='user_login')
def add_h_admin_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        h_admin_form = AddSWOForm(request.POST)
        if customer_form.is_valid() and h_admin_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = h_admin_form.cleaned_data['address']
            nida_number = h_admin_form.cleaned_data['nida_number']

            obj = User.objects.get(id=request.user.id)
            hr_obj = Human_resource_managers.objects.get(admin__user=obj)
            office_obj = hr_obj.office

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type=7)
            customer.save()

            staff = H_AdminHOD(admin=customer, address=address, office=office_obj, nida_number=nida_number)
            staff.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_h_admin')
    else:
        customer_form = AddCustomerForm()
        h_admin_form = AddSWOForm()
        context = {
            'customer_form': customer_form,
            'h_admin_form': h_admin_form
        }
        return render(request, 'hr_template/add_h_admin_template.html', context)


@login_required(login_url='user_login')
def manage_h_admin(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office_obj = hr_obj.office
    h_admins = H_AdminHOD.filter(office=office_obj)
    context = {
        "h_admins": h_admins
    }
    return render(request, 'hr_template/manage_h_admin_template.html', context)


@login_required(login_url='user_login')
def edit_h_admin(request, h_admin_id):
    # Adding Student ID into Session Variable
    request.session['h_admin_id'] = h_admin_id

    h_admin = H_AdminHOD.objects.get(admin=h_admin_id)
    form = EditSWOForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = h_admin.admin.user.email
    form.fields['username'].initial = h_admin.admin.user.username
    form.fields['first_name'].initial = h_admin.admin.user.first_name
    form.fields['last_name'].initial = h_admin.admin.user.last_name
    form.fields['address'].initial = h_admin.address

    context = {
        "id": h_admin_id,
        "username": h_admin.admin.user.username,
        "form": form
    }
    return render(request, "hr_template/edit_h_admin_template.html", context)


@login_required(login_url='user_login')
def edit_h_admin_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        h_admin_id = request.session.get('h_admin_id')
        if h_admin_id == None:
            return redirect('manage_h_admin')

        form = EditSWOForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']

            try:
                # First Update into Custom User Model
                user = H_AdminHOD.objects.get(id=h_admin_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username

                # Then Update Students Table

                user.address = address

                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['h_admin_id']

                messages.success(request, "Staff Updated Successfully!")
                return redirect('/edit_h_admin/' + h_admin_id)
            except:
                messages.success(request, "Failed to Update Staff.")
                return redirect('/edit_h_admin/' + h_admin_id)
        else:
            return redirect('/edit_h_admin/' + h_admin_id)


@login_required(login_url='user_login')
def delete_h_admin(request, h_admin_id):
    h_admin = H_AdminHOD.objects.get(id=h_admin_id)
    try:
        h_admin.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_h_admin')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_h_admin')


@login_required(login_url='user_login')
def add_admin(request):
    form = AddSWOForm()
    context = {
        "form": form
    }
    return render(request, 'hr_template/add_admin_template.html', context)


@login_required(login_url='user_login')
def add_admin_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        admin_form = AddSWOForm(request.POST)
        if customer_form.is_valid() and admin_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = admin_form.cleaned_data['address']
            nida_number = admin_form.cleaned_data['nida_number']

            obj = User.objects.get(id=request.user.id)
            hr_obj = Human_resource_managers.objects.get(admin__user=obj)
            office_obj = hr_obj.office

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type=8)
            customer.save()

            staff = AdminHOD(admin=customer, address=address, office=office_obj, nida_number=nida_number)
            staff.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_admin')
    else:
        customer_form = AddCustomerForm()
        admin_form = AddSWOForm()
        context = {
            'customer_form': customer_form,
            'admin_form': admin_form
        }
        return render(request, 'hr_template/add_admin_template.html', context)


@login_required(login_url='user_login')
def manage_admin(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office_obj = hr_obj.office
    admins = AdminHOD.filter(office=office_obj)
    context = {
        "admins": admins
    }
    return render(request, 'hr_template/manage_admin_template.html', context)


@login_required(login_url='user_login')
def edit_admin(request, admin_id):
    # Adding Student ID into Session Variable
    request.session['admin_id'] = admin_id

    admin = AdminHOD.objects.get(admin=admin_id)
    form = EditSWOForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = admin.admin.user.email
    form.fields['username'].initial = admin.admin.user.username
    form.fields['first_name'].initial = admin.admin.user.first_name
    form.fields['last_name'].initial = admin.admin.user.last_name
    form.fields['address'].initial = admin.address

    context = {
        "id": admin_id,
        "username": admin.admin.user.username,
        "form": form
    }
    return render(request, "hr_template/edit_admin_template.html", context)


@login_required(login_url='user_login')
def edit_admin_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        admin_id = request.session.get('admin_id')
        if admin_id == None:
            return redirect('manage_admin')

        form = EditSWOForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']

            try:
                # First Update into Custom User Model
                user = AdminHOD.objects.get(id=admin_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username

                # Then Update Students Table

                user.address = address

                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['admin_id']

                messages.success(request, "Staff Updated Successfully!")
                return redirect('/edit_admin/' + admin_id)
            except:
                messages.success(request, "Failed to Update Staff.")
                return redirect('/edit_admin/' + admin_id)
        else:
            return redirect('/edit_admin/' + admin_id)


@login_required(login_url='user_login')
def delete_admin(request, admin_id):
    admin = AdminHOD.objects.get(id=admin_id)
    try:
        admin.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return redirect('manage_admin')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return redirect('manage_admin')


@login_required(login_url='user_login')
def ceo_leave_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    leaves = LeaveReportCEO.objects.filter(ceo_id__office=office)
    context = {
        "leaves": leaves
    }
    return render(request, 'hr_template/ceo_leave_view.html', context)


@login_required(login_url='user_login')
def ceo_leave_approve(request, leave_id):
    leave = LeaveReportCEO.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('ceo_leave_view')


@login_required(login_url='user_login')
def ceo_leave_reject(request, leave_id):
    leave = LeaveReportCEO.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('ceo_leave_view')


@login_required(login_url='user_login')
def ceo_permission_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    permissions = PermissionReportCEO.objects.filter(ceo_id__office=office)
    context = {
        "permissions": permissions
    }
    return render(request, 'hr_template/ceo_permission_view.html', context)


@login_required(login_url='user_login')
def ceo_permission_approve(request, permission_id):
    permission = PermissionReportCEO.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('ceo_permission_view')


@login_required(login_url='user_login')
def ceo_permission_reject(request, permission_id):
    permission = PermissionReportCEO.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('ceo_permission_view')


@login_required(login_url='user_login')
def swo_leave_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    leaves = LeaveReportSWO.objects.filter(swo_id__office=office).order_by('swo_id')
    context = {
        "leaves": leaves
    }
    return render(request, 'hr_template/swo_leave_view.html', context)


@login_required(login_url='user_login')
def swo_leave_approve(request, leave_id):
    leave = LeaveReportSWO.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('swo_leave_view')


@login_required(login_url='user_login')
def swo_leave_reject(request, leave_id):
    leave = LeaveReportSWO.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('swo_leave_view')


@login_required(login_url='user_login')
def swo_permission_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    permissions = PermissionReportSWO.objects.filter(swo_id__office=office).order_by('swo_id')
    context = {
        "permissions": permissions
    }
    return render(request, 'hr_template/swo_permission_view.html', context)


@login_required(login_url='user_login')
def swo_permission_approve(request, permission_id):
    permission = PermissionReportSWO.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('swo_permission_view')


@login_required(login_url='user_login')
def swo_permission_reject(request, permission_id):
    permission = PermissionReportSWO.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('swo_permission_view')


@login_required(login_url='user_login')
def law_leave_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    leaves = LeaveReportLawyer.objects.all().order_by('lawyer_id')
    context = {
        "leaves": leaves
    }
    return render(request, 'hr_template/law_leave_view.html', context)


@login_required(login_url='user_login')
def law_leave_approve(request, leave_id):
    leave = LeaveReportLawyer.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('law_leave_view')


@login_required(login_url='user_login')
def law_leave_reject(request, leave_id):
    leave = LeaveReportLawyer.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('law_leave_view')


@login_required(login_url='user_login')
def law_permission_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    permissions = PermissionReportLawyer.objects.all().order_by('lawyer_id')
    context = {
        "permissions": permissions
    }
    return render(request, 'hr_template/law_permission_view.html', context)


@login_required(login_url='user_login')
def law_permission_approve(request, permission_id):
    permission = PermissionReportLawyer.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('law_permission_view')


@login_required(login_url='user_login')
def law_permission_reject(request, permission_id):
    permission = PermissionReportLawyer.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('law_permission_view')


@login_required(login_url='user_login')
def cs_leave_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    leaves = LeaveReportCS.objects.filter(cs_id__office=office).order_by('cs_id')
    context = {
        "leaves": leaves
    }
    return render(request, 'hr_template/cs_leave_view.html', context)


@login_required(login_url='user_login')
def cs_leave_approve(request, leave_id):
    leave = LeaveReportCS.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('cs_leave_view')


@login_required(login_url='user_login')
def cs_leave_reject(request, leave_id):
    leave = LeaveReportCS.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('cs_leave_view')


@login_required(login_url='user_login')
def cs_permission_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    permissions = PermissionReportCS.objects.filter(cs_id__office=office).order_by('cs_id')
    context = {
        "permissions": permissions
    }
    return render(request, 'hr_template/cs_permission_view.html', context)


@login_required(login_url='user_login')
def cs_permission_approve(request, permission_id):
    permission = PermissionReportCS.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('cs_permission_view')


@login_required(login_url='user_login')
def cs_permission_reject(request, permission_id):
    permission = PermissionReportCS.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('cs_permission_view')


@login_required(login_url='user_login')
def acc_leave_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    leaves = LeaveReportAccountant.objects.filter(accountant_id__office=office).order_by('accountant_id')
    context = {
        "leaves": leaves
    }
    return render(request, 'hr_template/acc_leave_view.html', context)


@login_required(login_url='user_login')
def acc_leave_approve(request, leave_id):
    leave = LeaveReportAccountant.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('acc_leave_view')


@login_required(login_url='user_login')
def acc_leave_reject(request, leave_id):
    leave = LeaveReportAccountant.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('acc_leave_view')


@login_required(login_url='user_login')
def acc_permission_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    permissions = PermissionReportAccountant.objects.filter(accountant_id__office=office).order_by('accountant_id')
    context = {
        "permissions": permissions
    }
    return render(request, 'hr_template/acc_permission_view.html', context)


@login_required(login_url='user_login')
def acc_permission_approve(request, permission_id):
    permission = PermissionReportAccountant.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('acc_permission_view')


@login_required(login_url='user_login')
def acc_permission_reject(request, permission_id):
    permission = PermissionReportAccountant.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('acc_permission_view')


@login_required(login_url='user_login')
def h_admin_leave_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    leaves = LeaveReportH_Admin.objects.filter(h_admin_id__office=office).order_by('h_admin_id')
    context = {
        "leaves": leaves
    }
    return render(request, 'hr_template/h_admin_leave_view.html', context)


@login_required(login_url='user_login')
def h_admin_leave_approve(request, leave_id):
    leave = LeaveReportH_Admin.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('h_admin_leave_view')


@login_required(login_url='user_login')
def h_admin_leave_reject(request, leave_id):
    leave = LeaveReportH_Admin.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('h_admin_leave_view')


@login_required(login_url='user_login')
def h_admin_permission_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    permissions = PermissionReportH_Admin.objects.filter(h_admin_id__office=office).order_by('h_admin_id')
    context = {
        "permissions": permissions
    }
    return render(request, 'hr_template/h_admin_permission_view.html', context)


@login_required(login_url='user_login')
def h_admin_permission_approve(request, permission_id):
    permission = PermissionReportH_Admin.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('h_admin_permission_view')


@login_required(login_url='user_login')
def h_admin_permission_reject(request, permission_id):
    permission = PermissionReportH_Admin.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('h_admin_permission_view')


@login_required(login_url='user_login')
def admin_leave_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    leaves = LeaveReportAdmin.objects.filter(admin_id__office=office).order_by('admin_id')
    context = {
        "leaves": leaves
    }
    return render(request, 'hr_template/admin_leave_view.html', context)


@login_required(login_url='user_login')
def admin_leave_approve(request, leave_id):
    leave = LeaveReportAdmin.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('admin_leave_view')


@login_required(login_url='user_login')
def admin_leave_reject(request, leave_id):
    leave = LeaveReportAdmin.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('admin_leave_view')


@login_required(login_url='user_login')
def admin_permission_view(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    permissions = PermissionReportAdmin.objects.filter(admin_id__office=office).order_by('admin_id')
    context = {
        "permissions": permissions
    }
    return render(request, 'hr_template/admin_permission_view.html', context)


@login_required(login_url='user_login')
def admin_permission_approve(request, permission_id):
    permission = PermissionReportAdmin.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('admin_permission_view')


@login_required(login_url='user_login')
def admin_permission_reject(request, permission_id):
    permission = PermissionReportAdmin.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('admin_permission_view')


@login_required(login_url='user_login')
def view_overdue(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    overdues = Overdue.objects.filter(office=office).order_by('name')
    context = {
        "overdues": overdues
    }
    return render(request, 'hr_template/view_overdue.html', context)


@login_required(login_url='user_login')
def view_ceo_salaries(request):
    salaries = SalaryCEO.objects.all()
    context = {
        "salaries": salaries
    }
    return render(request, 'hr_template/view_ceo_salaries.html', context)


@login_required(login_url='user_login')
def view_cs_salaries(request):
    salaries = SalaryCS.objects.all()
    context = {
        "salaries": salaries
    }
    return render(request, 'hr_template/view_cs_salaries.html', context)


@login_required(login_url='user_login')
def view_admin_salaries(request):
    salaries = SalaryAdmin.objects.all()
    context = {
        "salaries": salaries
    }
    return render(request, 'hr_template/view_admin_salaries.html', context)


@login_required(login_url='user_login')
def view_law_salaries(request):
    salaries = SalaryLawyer.objects.all()
    context = {
        "salaries": salaries
    }
    return render(request, 'hr_template/view_law_salaries.html', context)


@login_required(login_url='user_login')
def view_swo_salaries(request):
    salaries = SalarySWO.objects.all()
    context = {
        "salaries": salaries
    }
    return render(request, 'hr_template/view_swo_salaries.html', context)


@login_required(login_url='user_login')
def view_acc_salaries(request):
    salaries = SalaryAccountant.objects.all()
    context = {
        "salaries": salaries
    }
    return render(request, 'hr_template/view_acc_salaries.html', context)


@login_required(login_url='user_login')
def view_hr_salaries(request):
    salaries = SalaryHR.objects.all()
    context = {
        "salaries": salaries
    }
    return render(request, 'hr_template/view_hr_salaries.html', context)


@login_required(login_url='user_login')
def hr_view_acc_resp(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    resps = ResponsibilityAccountant.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'hr_template/view_acc_resp.html', context)


@login_required(login_url='user_login')
def hr_view_admin_resp(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    resps = ResponsibilityAdmin.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'hr_template/view_admin_resp.html', context)


@login_required(login_url='user_login')
def hr_view_swo_resp(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    resps = ResponsibilitySWO.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'hr_template/view_swo_resp.html', context)


@login_required(login_url='user_login')
def hr_view_cs_resp(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    resps = ResponsibilityCS.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'hr_template/view_cs_resp.html', context)


@login_required(login_url='user_login')
def hr_view_law_resp(request):
    resps = ResponsibilityLawyers.objects.all()
    context = {
        "resps": resps
    }
    return render(request, 'hr_template/view_law_resp.html', context)


@login_required(login_url='user_login')
def hr_view_hr_resp(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    resps = ResponsibilityHR.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'hr_template/view_hr_resp.html', context)


@login_required(login_url='user_login')
def hr_view_ceo_resp(request):
    resps = ResponsibilityCEO.objects.all()
    context = {
        "resps": resps
    }
    return render(request, 'hr_template/view_ceo_resp.html', context)


@login_required(login_url='user_login')
def hr_view_goals(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    goals = Goals.objects.filter(office=office)
    context = {
        "goals": goals
    }
    return render(request, 'hr_template/view_goals.html', context)


@login_required(login_url='user_login')
def hr_view_code(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=obj)
    office = hr_obj.office
    codes = Code_of_Conduct.objects.filter(office=office)
    context = {
        "codes": codes
    }
    return render(request, 'hr_template/view_codes.html', context)


@login_required(login_url='user_login')
def hr_feedback(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    feedback_data = FeedBackHR.objects.filter(hr_id=hr_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'hr_template/hr_feedback.html', context)


@login_required(login_url='user_login')
def hr_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('hr_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        hr_obj = Human_resource_managers.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackHR(hr_id=hr_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('hr_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('hr_feedback')


@login_required(login_url='user_login')
def hr_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    leave_data = LeaveReportHR.objects.filter(hr_id=hr_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'hr_template/hr_apply_leave.html', context)


@login_required(login_url='user_login')
def hr_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('hr_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        hr_obj = Human_resource_managers.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportHR(hr_id=hr_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('hr_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('hr_apply_leave')


@login_required(login_url='user_login')
def hr_apply_permission(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    permission_data = PermissionReportHR.objects.filter(hr_id=hr_obj)
    context = {
        "permission_data": permission_data
    }
    return render(request, 'hr_template/hr_apply_permission.html', context)


@login_required(login_url='user_login')
def hr_apply_permission_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('hr_permission_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        hr_obj = Human_resource_managers.objects.get(admin__user=user)
        try:
            leave_report = PermissionReportHR(hr_id=hr_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Permission.")
            return redirect('hr_apply_permission')
        except:
            messages.error(request, "Failed to Apply Permission")
            return redirect('hr_apply_permission')


@login_required(login_url='user_login')
def hr_view_notification(request):
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    notifications = NotificationHR.objects.filter(hr_id=hr.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "hr_template/hr_view_notification.html", context)


@login_required(login_url='user_login')
def hr_view_def_notification(request):
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    def_notifications = DefendantNotificationHR.objects.filter(hr_id=hr.id)
    context = {
        "notifications": def_notifications,
    }
    return render(request, "hr_template/hr_view_def_notification.html", context)


@login_required(login_url='user_login')
def hr_view_acu_notification(request):
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    acu_notifications = AccuserNotificationHR.objects.filter(hr_id=hr.id)
    context = {
        "notifications": acu_notifications,
    }
    return render(request, "hr_template/hr_view_acu_notification.html", context)


@login_required(login_url='user_login')
def hr_add_notification_ceo(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    ceos = CEO.objects.all()
    context = {
        "ceos": ceos
    }
    return render(request, 'hr_template/add_ceo_notification_template.html', context)


@login_required(login_url='user_login')
def view_ceo(request):
    ceos = CEO.objects.all()
    context = {
        "ceos": ceos
    }
    return render(request, 'hr_template/view_ceo_template.html', context)


@login_required(login_url='user_login')
def hr_add_notification_ceo_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_ceo')
    else:
        message = request.POST.get('message')

        ceo_id = request.POST.get('ceo')
        ceo = CEO.objects.get(id=ceo_id)

        try:
            notification = NotificationCEO(message=message, ceo_id=ceo)
            notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_ceo')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_ceo')


@login_required(login_url='user_login')
def hr_manage_notification_ceo(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    notifications = NotificationCEO.objects.all()
    context = {
        "notifications": notifications
    }
    return render(request, 'hr_template/manage_ceo_notification_template.html', context)


@login_required(login_url='user_login')
def hr_edit_notification_ceo(request, ceo_id):
    request.session['ceo_id'] = ceo_id

    ceo = CEO.objects.get(id=ceo_id)
    context = {
        "ceo": ceo,
        "id": ceo_id
    }
    return render(request, 'hr_template/edit_ceo_notification_template.html', context)


@login_required(login_url='user_login')
def hr_edit_notification_ceo_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        ceo_id = request.session.get('ceo_id')
        message = request.POST.get('message')
        ceo = CEO.objects.get(id=ceo_id)

        try:
            ceo_notification = NotificationCEO(message=message, ceo_id=ceo)
            ceo_notification.save()

            del request.session['ceo_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_ceo/' + ceo_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_ceo/' + ceo_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def hr_delete_notification_ceo(request, notification_id):
    notification = NotificationCEO.objects.get(id=notification_id)
    try:
        notification.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_ceo')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_ceo')


@login_required(login_url='user_login')
def add_notification_swo(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    swos = Social_welfare_officers.objects.filter(office=office)
    context = {
        "swos": swos
    }
    return render(request, 'hr_template/add_swo_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_swo_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_swo')
    else:
        message = request.POST.get('message')

        swo_id = request.POST.get('swo')
        swo = Social_welfare_officers.objects.get(id=swo_id)

        try:
            notification = NotificationSWO(message=message, swo_id=swo)
            notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_swo')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_swo')


@login_required(login_url='user_login')
def manage_notification_swo(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    notifications = NotificationSWO.objects.filter(swo_id__office=office)
    context = {
        "notifications": notifications
    }
    return render(request, 'hr_template/manage_swo_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_swo(request, swo_id):
    request.session['swo_id'] = swo_id

    swo = Social_welfare_officers.objects.get(id=swo_id)
    context = {
        "swo": swo,
        "id": swo_id
    }
    return render(request, 'hr_template/edit_swo_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_swo_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        swo_id = request.session.get('swo_id')
        message = request.POST.get('message')
        swo = Social_welfare_officers.objects.get(id=swo_id)

        try:
            notification = NotificationSWO(message=message, swo_id=swo)
            notification.save()

            del request.session['swo_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_swo/' + swo_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_swo/' + swo_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_swo(request, notification_id):
    notification = NotificationSWO.objects.get(id=notification_id)
    try:
        notification.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_swo')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_swo')


@login_required(login_url='user_login')
def add_notification_law(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    laws = Lawyers.objects.all()
    context = {
        "laws": laws
    }
    return render(request, 'hr_template/add_law_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_law_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_law')
    else:
        message = request.POST.get('message')

        law_id = request.POST.get('law')
        law = Lawyers.objects.get(id=law_id)

        try:
            notification = NotificationLawyer(message=message, lawyer_id=law)
            notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_law')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_law')


@login_required(login_url='user_login')
def manage_notification_law(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    notifications = NotificationLawyer.objects.all()
    context = {
        "notifications": notifications
    }
    return render(request, 'hr_template/manage_law_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_law(request, law_id):
    request.session['law_id'] = law_id

    law = Lawyers.objects.get(id=law_id)
    context = {
        "law": law,
        "id": law_id
    }
    return render(request, 'hr_template/edit_law_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_law_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        law_id = request.session.get('law_id')
        message = request.POST.get('message')
        law = Lawyers.objects.get(id=law_id)

        try:
            notification = NotificationLawyer(message=message, lawyer_id=law)
            notification.save()

            del request.session['law_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_law/' + law_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_law/' + law_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_law(request, notification_id):
    notification = NotificationLawyer.objects.get(id=notification_id)
    try:
        notification.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_law')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_law')


@login_required(login_url='user_login')
def add_notification_cs(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    css = Customer_service.objects.filter(office=office)
    context = {
        "css": css
    }
    return render(request, 'hr_template/add_cs_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_cs_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_cs')
    else:
        message = request.POST.get('message')

        cs_id = request.POST.get('cs')
        cs = Customer_service.objects.get(id=cs_id)

        try:
            notification = NotificationCS(message=message, cs_id=cs)
            notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_cs')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_cs')


@login_required(login_url='user_login')
def manage_notification_cs(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    notifications = NotificationCS.objects.filter(cs_id__office=office)
    context = {
        "notifications": notifications
    }
    return render(request, 'hr_template/manage_cs_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_cs(request, cs_id):
    request.session['cs_id'] = cs_id

    cs = Customer_service.objects.get(id=cs_id)
    context = {
        "cs": cs,
        "id": cs_id
    }
    return render(request, 'hr_template/edit_cs_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_cs_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        cs_id = request.session.get('cs_id')
        message = request.POST.get('message')
        cs = Customer_service.objects.get(id=cs_id)

        try:
            notification = NotificationCS(message=message, cs_id=cs)
            notification.save()

            del request.session['cs_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_cs/' + cs_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_cs/' + cs_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_cs(request, notification_id):
    notification = NotificationCS.objects.get(id=notification_id)
    try:
        notification.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_cs')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_cs')


@login_required(login_url='user_login')
def add_notification_acc(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    accs = Accountant.objects.filter(office=office)
    context = {
        "accs": accs
    }
    return render(request, 'hr_template/add_acc_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_acc_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_acc')
    else:
        message = request.POST.get('message')

        acc_id = request.POST.get('acc')
        acc = Accountant.objects.get(id=acc_id)

        try:
            notification = NotificationAccountant(message=message, accountant_id=acc)
            notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_acc')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_acc')


@login_required(login_url='user_login')
def manage_notification_acc(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    notifications = NotificationAccountant.objects.filter(accountant_id__office=office)
    context = {
        "notifications": notifications
    }
    return render(request, 'hr_template/manage_acc_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_acc(request, acc_id):
    request.session['acc_id'] = acc_id

    acc = Accountant.objects.get(id=acc_id)
    context = {
        "acc": acc,
        "id": acc_id
    }
    return render(request, 'hr_template/edit_acc_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_acc_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        acc_id = request.session.get('acc_id')
        message = request.POST.get('message')
        acc = Accountant.objects.get(id=acc_id)

        try:
            notification = NotificationAccountant(message=message, accountant_id=acc)
            notification.save()

            del request.session['swo_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_acc/' + acc_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_acc/' + acc_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_acc(request, notification_id):
    notification = NotificationAccountant.objects.get(id=notification_id)
    try:
        notification.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_acc')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_acc')


@login_required(login_url='user_login')
def add_notification_h_admin(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    h_admins = H_AdminHOD.objects.filter(office=office)
    context = {
        "h_admins": h_admins
    }
    return render(request, 'hr_template/add_h_admin_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_h_admin_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_h_admin')
    else:
        message = request.POST.get('message')

        h_admin_id = request.POST.get('h_admin')
        h_admin = H_AdminHOD.objects.get(id=h_admin_id)

        try:
            notification = NotificationH_Admin(message=message, h_admin_id=h_admin)
            notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_h_admin')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_h_admin')


@login_required(login_url='user_login')
def manage_notification_h_admin(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    notifications = NotificationH_Admin.objects.filter(h_admin_id__office=office)
    context = {
        "notifications": notifications
    }
    return render(request, 'hr_template/manage_h_admin_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_h_admin(request, h_admin_id):
    request.session['h_admin_id'] = h_admin_id

    h_admin = H_AdminHOD.objects.get(id=h_admin_id)
    context = {
        "h_admin": h_admin,
        "id": h_admin_id
    }
    return render(request, 'hr_template/edit_h_admin_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_h_admin_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        h_admin_id = request.session.get('h_admin_id')
        message = request.POST.get('message')
        h_admin = H_AdminHOD.objects.get(id=h_admin_id)

        try:
            notification = NotificationH_Admin(message=message, h_admin_id=h_admin)
            notification.save()

            del request.session['h_admin_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_h_admin/' + h_admin_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_h_admin/' + h_admin_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_h_admin(request, notification_id):
    notification = NotificationH_Admin.objects.get(id=notification_id)
    try:
        notification.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_h_admin')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_h_admin')


@login_required(login_url='user_login')
def add_notification_admin(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    admins = AdminHOD.objects.filter(office=office)
    context = {
        "admins": admins
    }
    return render(request, 'hr_template/add_admin_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_admin_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_admin')
    else:
        message = request.POST.get('message')

        admin_id = request.POST.get('admin')
        admin = AdminHOD.objects.get(id=admin_id)

        try:
            notification = NotificationAdmin(message=message, admin_id=admin)
            notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_admin')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_admin')


@login_required(login_url='user_login')
def manage_notification_admin(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    notifications = NotificationAdmin.objects.filter(admin_id__office=office)
    context = {
        "notifications": notifications
    }
    return render(request, 'hr_template/manage_admin_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_admin(request, admin_id):
    request.session['admin_id'] = admin_id

    admin = AdminHOD.objects.get(id=admin_id)
    context = {
        "admin": admin,
        "id": admin_id
    }
    return render(request, 'hr_template/edit_admin_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_admin_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        admin_id = request.session.get('admin_id')
        message = request.POST.get('message')
        admin = AdminHOD.objects.get(id=admin_id)

        try:
            notification = NotificationAdmin(message=message, admin_id=admin)
            notification.save()

            del request.session['admin_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_admin/' + admin_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_admin/' + admin_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_admin(request, notification_id):
    notification = NotificationAdmin.objects.get(id=notification_id)
    try:
        notification.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_admin')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_admin')


@login_required(login_url='user_login')
def add_hr_meeting(request):
    return render(request, "hr_template/add_hr_meeting_template.html")


@login_required(login_url='user_login')
def add_hr_meeting_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_hr_meeting')
    else:
        user = User.objects.get(id=request.user.id)
        hr_obj = Human_resource_managers.objects.get(admin__user=user)
        office = hr_obj.office
        name = request.POST.get('name')
        date = request.POST.get('date')
        try:
            meeting_model = HRMeeting(meeting_name=name, office=office, date=date)
            meeting_model.save()
            messages.success(request, "Meeting Added Successfully!")
            return redirect('add_hr_meeting')
        except:
            messages.error(request, "Failed to Add Meeting!")
            return redirect('add_hr_meeting')


@login_required(login_url='user_login')
def manage_hr_meeting(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    meetings = HRMeeting.objects.filter(office=office)
    context = {
        "meetings": meetings
    }
    return render(request, 'hr_template/manage_hr_meeting_template.html', context)


@login_required(login_url='user_login')
def edit_hr_meeting(request, meeting_id):
    request.session['meeting_id'] = meeting_id
    meeting = HRMeeting.objects.get(id=meeting_id)
    context = {
        "meeting": meeting,
        "id": meeting_id
    }
    return render(request, 'hr_template/edit_hr_meeting_template.html', context)


@login_required(login_url='user_login')
def edit_hr_meeting_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        hr_meeting_id = request.session.get('hr_meeting_id')
        name = request.POST.get('name')
        date = request.POST.get('date')

        try:
            meeting = HRMeeting.objects.get(id=hr_meeting_id)
            meeting.meeting_name = name
            meeting.date = date
            meeting.save()

            messages.success(request, "Meeting Updated Successfully.")
            return redirect('/edit_hr_meeting/'+hr_meeting_id)

        except:
            messages.error(request, "Failed to Update Meeting.")
            return redirect('/edit_hr_meeting/'+hr_meeting_id)


@login_required(login_url='user_login')
def delete_hr_meeting(request, meeting_id):
    meeting = HRMeeting.objects.get(id=meeting_id)
    topics = HRTopics.objects.filter(meeting_id = meeting)
    attendances = AttendanceHRReport.objects.filter(meeting_id=meeting)
    try:
        for topic in topics:
            topic.delete()
        for attendance in attendances:
            attendance.delete()
        meeting.delete()
        messages.success(request, "Meeting Deleted Successfully.")
        return redirect('manage_hr_meeting')
    except:
        messages.error(request, "Failed to Delete Meeting.")
        return redirect('manage_hr_meeting')


@login_required(login_url='user_login')
def add_hr_topics(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    meetings = HRMeeting.objects.filter(office=office)
    context = {
        "meetings": meetings,
    }
    return render(request, 'hr_template/add_topic_template.html', context)


@login_required(login_url='user_login')
def add_hr_topics_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_hr_topics')
    else:
        user = User.objects.get(id=request.user.id)
        hr_obj = Human_resource_managers.objects.get(admin__user=user)
        topic_name = request.POST.get('topic')

        meeting_id = request.POST.get('meeting')
        meeting = HRMeeting.objects.get(id=meeting_id)

        try:
            topic = HRTopics(topic_name=topic_name, meeting_id=meeting, hr_id=hr_obj)
            topic.save()
            messages.success(request, "Agenda Added Successfully!")
            return redirect('add_hr_topics')
        except:
            messages.error(request, "Failed to Add Agenda!")
            return redirect('add_hr_topics')


@login_required(login_url='user_login')
def manage_hr_topics(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    topics = HRTopics.objects.filter(hr_id=hr_obj)
    context = {
        "topics": topics
    }
    return render(request, 'hr_template/manage_topic_template.html', context)


@login_required(login_url='user_login')
def edit_hr_topics(request, topic_id):
    request.session['topic_id'] = topic_id
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    office = hr_obj.office
    topic = HRTopics.objects.get(id=topic_id)
    meetings = HRMeeting.objects.filter(office=office)
    context = {
        "topic": topic,
        "meetings": meetings,
        "id": topic_id
    }
    return render(request, 'hr_template/edit_topic_template.html', context)


@login_required(login_url='user_login')
def edit_hr_topics_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        topic_id = request.session.get('topic_id')
        topic_name = request.POST.get('topic')
        meeting_id = request.POST.get('meeting')

        try:
            topic = HRTopics.objects.get(id=topic_id)
            topic.topic_name = topic_name

            meeting = HRMeeting.objects.get(id=meeting_id)
            topic.meeting_id = meeting
            topic.save()

            messages.success(request, "Agenda Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_hr_topic", kwargs={"topic_id": topic_id}))

        except:
            messages.error(request, "Failed to Update Agenda.")
            return HttpResponseRedirect(reverse("edit_hr_topic", kwargs={"topic_id": topic_id}))
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_hr_topics(request, topic_id):
    topic = HRTopics.objects.get(id=topic_id)
    try:
        topic.delete()
        messages.success(request, "Topic Deleted Successfully.")
        return redirect('manage_hr_topic')
    except:
        messages.error(request, "Failed to Delete Topic.")
        return redirect('manage_hr_topic')


@login_required(login_url='user_login')
def hr_take_attendance(request, meeting_id):
    request.session['meeting_id'] = meeting_id

    meeting = HRMeeting.objects.get(id=meeting_id)
    attendances = AttendanceHRReport.objects.filter(meeting_id=meeting)

    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    office = hr.office
    ceos = CEO.objects.filter(office=office)
    swos = Social_welfare_officers.objects.filter(office=office)
    accs = Accountant.objects.filter(office=office)
    hrs = Human_resource_managers.objects.filter(office=office)
    lawyers = Lawyers.objects.all()
    css = Customer_service.objects.filter(office=office)
    admins = AdminHOD.objects.filter(office=office)
    h_admins = H_AdminHOD.objects.filter(office=office)

    context = {
        "attendances": attendances,
        "meeting": meeting,
        "id": meeting_id,
        "ceos": ceos,
        "swos": swos,
        "accs": accs,
        "hrs": hrs,
        "lawyers": lawyers,
        "css": css,
        "admins": admins,
        "h_admins": h_admins,
    }
    return render(request, "hr_template/take_attendance_template.html", context)


@login_required(login_url='user_login')
def hr_meeting_attendance_approve(request, attendance_id):
    att = AttendanceHRReport.objects.get(id=attendance_id)
    att.status = 1
    att.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def hr_meeting_attendance_reject(request, attendance_id):
    att = AttendanceHRReport.objects.get(id=attendance_id)
    att.status = 2
    att.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def ceo_attend_hr_save(request, ceo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = CEO.objects.get(id=ceo_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def ceo_not_attend_hr_save(request, ceo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = CEO.objects.get(id=ceo_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def hr_attend_hr_save(request, hr_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Human_resource_managers.objects.get(id=hr_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def hr_not_attend_hr_save(request, hr_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Human_resource_managers.objects.get(id=hr_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def swo_attend_hr_save(request, swo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Social_welfare_officers.objects.get(id=swo_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def swo_not_attend_hr_save(request, swo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Social_welfare_officers.objects.get(id=swo_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def law_attend_hr_save(request, law_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Lawyers.objects.get(id=law_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def law_not_attend_hr_save(request, law_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Lawyers.objects.get(id=law_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def cs_attend_hr_save(request, cs_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Customer_service.objects.get(id=cs_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def cs_not_attend_hr_save(request, cs_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Customer_service.objects.get(id=cs_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def acc_attend_hr_save(request, acc_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Accountant.objects.get(id=acc_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def acc_not_attend_hr_save(request, acc_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = Accountant.objects.get(id=acc_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def h_admin_attend_hr_save(request, h_admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = H_AdminHOD.objects.get(id=h_admin_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def h_admin_not_attend_hr_save(request, h_admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = H_AdminHOD.objects.get(id=h_admin_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def admin_attend_hr_save(request, admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = AdminHOD.objects.get(id=admin_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def admin_not_attend_hr_save(request, admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = HRMeeting.objects.get(id=meeting_id)
    att = AdminHOD.objects.get(id=admin_id)
    attendant_id = att.admin

    attendance = AttendanceHRReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('hr_take_attendance')


@login_required(login_url='user_login')
def hr_profile(request):
    user = User.objects.get(id=request.user.id)
    hr_obj = Human_resource_managers.objects.get(admin__user=user)
    context={
        "user": user,
        "hr": hr_obj,
    }
    return render(request, 'hr_template/hr_profile.html', context)


@login_required(login_url='user_login')
def hr_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('hr_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.get(id=request.user.id)
            hr_obj = Human_resource_managers.objects.get(admin__user=user)
            customuser = S_CustomUser.objects.get(user=user)
            customuser.user.first_name = first_name
            customuser.user.last_name = last_name
            customuser.user.email = email
            customuser.user.username = username
            if password != None and password != "":
                customuser.user.set_password(password)
            customuser.save()
            hr_obj.address = address
            hr_obj.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('hr_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('hr_profile')


@login_required(login_url='user_login')
def add_disc_comm(request):
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    office = hr.office
    region = office.region
    ceos = CEO.objects.filter(office=office)
    swos = Social_welfare_officers.objects.filter(office=office)
    accs = Accountant.objects.filter(office=office)
    hrs = Human_resource_managers.objects.filter(office=office)
    lawyers = Lawyers.objects.all()
    css = Customer_service.objects.filter(office=office)
    drivers = Drivers.objects.filter(region=region)
    h_drivers = H_Drivers.objects.filter(region=region)
    admins = AdminHOD.objects.filter(office=office)
    h_admins = H_AdminHOD.objects.filter(office=office)

    context = {
        "ceos": ceos,
        "swos": swos,
        "accs": accs,
        "hrs": hrs,
        "lawyers": lawyers,
        "css": css,
        "drivers": drivers,
        "admins": admins,
        "h_admins": h_admins,
    }
    return render(request, "hr_template/add_disc_comm_template.html", context)


@login_required(login_url='user_login')
def add_disc_comm_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_disc_comm')
    else:
        user = User.objects.get(id=request.user.id)
        hr = Human_resource_managers.objects.get(admin__user=user)
        office = hr.office

        ceo_id = request.POST.get('ceo')
        swo_id = request.POST.get('swo')
        acc_id = request.POST.get('acc')
        hr_id = request.POST.get('hr')
        lawyer_id = request.POST.get('lawyer')
        cs_id = request.POST.get('cs')
        driver_id = request.POST.get('driver')
        admin_id = request.POST.get('admin')
        h_admin_id = request.POST.get('h_admin')

        ceo = CEO.objects.get(id=ceo_id)
        swo = Social_welfare_officers.objects.get(id=swo_id)
        acc = Accountant.objects.get(id=acc_id)
        hr = Human_resource_managers.objects.get(id=hr_id)
        lawyer = Lawyers.objects.get(id=lawyer_id)
        cs = Customer_service.objects.get(id=cs_id)
        driver = Drivers.objects.get(id=driver_id)
        admin = AdminHOD.objects.get(id=admin_id)
        h_admin = H_AdminHOD.objects.get(id=h_admin_id)
        s_name = hr.admin

        try:
            disc_comm = Discpline_committee(office=office, s_name=s_name, ceo=ceo, hr=hr, apartment_driver=driver, hotel_admin=h_admin, apartment_admin=admin,
                                            lawyer=lawyer, accountant=acc, cs=cs, swo=swo)
            disc_comm.save()
            messages.success(request, "Discpline Committee Added Successfully!")
            return redirect('add_disc_comm')
        except:
            messages.error(request, "Failed to Add Discpline Committee!")
            return redirect('add_disc_comm')


@login_required(login_url='user_login')
def manage_disc_comm(request):
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    office = hr.office
    disc_comms = Discpline_committee.objects.filter(office=office)
    context = {
        "disc_comms": disc_comms
    }
    return render(request, 'hr_template/manage_disc_comm_template.html', context)


@login_required(login_url='user_login')
def edit_disc_comm(request, disc_comm_id):
    request.session['disc_comm_id'] = disc_comm_id
    disc_comm = Discpline_committee.objects.get(id=disc_comm_id)
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    office = hr.office
    region = office.region
    ceos = CEO.objects.filter(office=office)
    swos = Social_welfare_officers.objects.filter(office=office)
    accs = Accountant.objects.filter(office=office)
    hrs = Human_resource_managers.objects.filter(office=office)
    lawyers = Lawyers.objects.all()
    css = Customer_service.objects.filter(office=office)
    drivers = Drivers.objects.filter(region=region)
    admins = AdminHOD.objects.filter(office=office)
    h_admins = H_AdminHOD.objects.filter(office=office)

    context = {
        "disc_comm": disc_comm,
        "id": disc_comm_id,
        "ceos": ceos,
        "swos": swos,
        "accs": accs,
        "hrs": hrs,
        "lawyers": lawyers,
        "css": css,
        "drivers": drivers,
        "admins": admins,
        "h_admins": h_admins,
    }
    return render(request, "hr_template/edit_disc_comm_template.html", context)


@login_required(login_url='user_login')
def edit_disc_comm_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('edit_disc_comm')
    else:
        user = User.objects.get(id=request.user.id)
        hr = Human_resource_managers.objects.get(admin__user=user)
        office = hr.office

        disc_comm_id = request.session.get('disc_comm_id')
        disc_comm = Discpline_committee.objects.get(id=disc_comm_id)

        category = request.POST.get('category')
        ceo_id = request.POST.get('ceo')
        swo_id = request.POST.get('swo')
        acc_id = request.POST.get('acc')
        hr_id = request.POST.get('hr')
        lawyer_id = request.POST.get('lawyer')
        cs_id = request.POST.get('cs')
        driver_id = request.POST.get('driver')
        admin_id = request.POST.get('admin')
        h_admin_id = request.POST.get('h_admin')


        try:
            ceo = CEO.objects.get(id=ceo_id)
            swo = Social_welfare_officers.objects.get(id=swo_id)
            acc = Accountant.objects.get(id=acc_id)
            hr = Human_resource_managers.objects.get(id=hr_id)
            lawyer = Lawyers.objects.get(id=lawyer_id)
            cs = Customer_service.objects.get(id=cs_id)
            driver = Drivers.objects.get(id=driver_id)
            admin = AdminHOD.objects.get(id=admin_id)
            h_admin = H_AdminHOD.objects.get(id=h_admin_id)
            s_name = hr.admin

            disc_comm.ceo = ceo
            disc_comm.s_name = s_name
            disc_comm.swo = swo
            disc_comm.accountant = acc
            disc_comm.hr = hr
            disc_comm.lawyer = lawyer
            disc_comm.cs = cs
            disc_comm.apartment_driver = driver
            disc_comm.hotel_admin = h_admin
            disc_comm.apartment_admin = admin
            if category == 'CEO':
                disc_comm.h_name = ceo.admin
            elif category == 'SWO':
                disc_comm.h_name = swo.admin
            elif category == 'Accountant':
                disc_comm.h_name = acc.admin
            elif category == 'Lawyer':
                disc_comm.h_name = lawyer.admin
            elif category == 'Customer Service':
                disc_comm.h_name = cs.admin
            elif category == 'Apartment Driver':
                disc_comm.h_name = driver.admin
            elif category == 'Hotel Admin':
                disc_comm.h_name = h_admin.admin
            elif category == 'Apartment Admin':
                disc_comm.h_name = admin.admin
            else:
                disc_comm.h_name = ""
            disc_comm.save()

            messages.success(request, "Discpline Committee Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_disc_comm", kwargs={"disc_comm_id": disc_comm_id}))

        except:
            messages.error(request, "Failed to Update Discpline Committee.")
            return HttpResponseRedirect(reverse("edit_disc_comm", kwargs={"disc_comm_id": disc_comm_id}))


@login_required(login_url='user_login')
def delete_disc_comm(request, disc_comm_id):
    disc_comm = Discpline_committee.objects.get(id=disc_comm_id)
    try:
        disc_comm.delete()
        messages.success(request, "Discpline Committee Deleted Successfully.")
        return redirect('manage_disc_comm')
    except:
        messages.error(request, "Failed to Delete Discpline Committee.")
        return redirect('manage_disc_comm')


@login_required(login_url='user_login')
def add_disc_meeting(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office
    region = office.region
    ceos = CEO.objects.filter(office=office)
    swos = Social_welfare_officers.objects.filter(office=office)
    accs = Accountant.objects.filter(office=office)
    hrs = Human_resource_managers.objects.filter(office=office)
    lawyers = Lawyers.objects.all()
    css = Customer_service.objects.filter(office=office)
    drivers = Drivers.objects.filter(region=region)
    admins = AdminHOD.objects.filter(office=office)
    h_admins = H_AdminHOD.objects.filter(office=office)
    context = {
        "ceos": ceos,
        "swos": swos,
        "accs": accs,
        "hrs": hrs,
        "lawyers": lawyers,
        "css": css,
        "drivers": drivers,
        "admins": admins,
        "h_admins": h_admins,
    }
    return render(request, 'hr_template/add_disc_meeting_template.html', context)


@login_required(login_url='user_login')
def add_disc_meeting_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_disc_meeting')
    else:
        user = User.objects.get(id=request.user.id)
        acc = Human_resource_managers.objects.get(admin__user=user)
        office = acc.office

        acu_category = request.POST.get("acu_category")
        def_category = request.POST.get("def_category")
        date = request.POST.get('date')
        accusation = request.POST.get('accusation')
        def_name_id = request.POST.get('def_name')
        acu_name_id = request.POST.get('acu_name')

        defendant_name = S_CustomUser.objects.get(id=def_name_id.admin)
        accuser_name = S_CustomUser.objects.get(id=acu_name_id.admin)

        try:
            disc_meeting = DiscplineMeeting(office=office, date=date, defendant_name=defendant_name,
                                            accuser_name=accuser_name, accusation=accusation, status=False)
            disc_meeting.save()
            if def_category == 'CEO':
                ceo_id = CEO.objects.get(id=def_name_id)
                notification = DefendantNotificationCEO(ceo_id=ceo_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'SWO':
                swo_id = Social_welfare_officers.objects.get(id=def_name_id)
                notification = DefendantNotificationSWO(swo_id=swo_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'Accountant':
                accountant_id = Accountant.objects.get(id=def_name_id)
                notification = DefendantNotificationAccountant(accountant_id=accountant_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'HR':
                hr_id = Human_resource_managers.objects.get(id=def_name_id)
                notification = DefendantNotificationHR(hr_id=hr_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'Lawyer':
                lawyer_id = Lawyers.objects.get(id=def_name_id)
                notification = DefendantNotificationLawyer(lawyer_id=lawyer_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'Customer Service':
                cs_id = Customer_service.objects.get(id=def_name_id)
                notification = DefendantNotificationCS(cs_id=cs_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'Apartment Driver':
                driver_id = Drivers.objects.get(id=def_name_id)
                notification = DefendantNotificationDriver(driver_id=driver_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'Apartment Admin':
                admin_id = AdminHOD.objects.get(id=def_name_id)
                notification = DefendantNotificationAdmin(admin_id=admin_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            elif def_category == 'Hotel Admin':
                h_admin_id = H_AdminHOD.objects.get(id=def_name_id)
                notification = DefendantNotificationH_Admin(h_admin_id=h_admin_id, message=accusation)
                notification.save()
                messages.success(request, "Defendant Notification Added Successfully!")
            else:
                messages.success(request, "Failed to Add Defendant Notification!")

            if acu_category == 'CEO':
                ceo_id = CEO.objects.get(id=acu_name_id)
                notification = AccusserNotificationCEO(ceo_id=ceo_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'SWO':
                swo_id = Social_welfare_officers.objects.get(id=acu_name_id)
                notification = AccusserNotificationSWO(swo_id=swo_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'Accountant':
                accountant_id = Accountant.objects.get(id=acu_name_id)
                notification = AccusserNotificationAccountant(accountant_id=accountant_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'HR':
                hr_id = Human_resource_managers.objects.get(id=acu_name_id)
                notification = AccuserNotificationHR(hr_id=hr_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'Lawyer':
                lawyer_id = Lawyers.objects.get(id=acu_name_id)
                notification = AccusserNotificationLawyer(lawyer_id=lawyer_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'Customer Service':
                cs_id = Customer_service.objects.get(id=acu_name_id)
                notification = AccusserNotificationCS(cs_id=cs_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'Apartment Driver':
                driver_id = Drivers.objects.get(id=acu_name_id)
                notification = AccusserNotificationDriver(driver_id=driver_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'Apartment Admin':
                admin_id = AdminHOD.objects.get(id=acu_name_id)
                notification = AccusserNotificationAdmin(admin_id=admin_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            elif acu_category == 'Hotel Admin':
                h_admin_id = H_AdminHOD.objects.get(id=acu_name_id)
                notification = AccusserNotificationH_Admin(h_admin_id=h_admin_id, message=accusation)
                notification.save()
                messages.success(request, "Accusation Notification Added Successfully!")
            else:
                messages.success(request, "Failed to Add Accusation Notification!")
            messages.success(request, "Discpline Meeting Added Successfully!")
            return redirect('add_disc_meeting')
        except:
            messages.error(request, "Failed to Add Discpline Meeting!")
            return redirect('add_disc_meeting')


@login_required(login_url='user_login')
def arranged_disc_meeting_view(request):
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    office = hr.office
    disc_meetings = DiscplineMeeting.objects.filter(office=office, status=False)
    context = {
        "disc_meetings": disc_meetings
    }
    return render(request, 'hr_template/disc_meeting_view.html', context)


@login_required(login_url='user_login')
def conclude_disc_meeting_view(request, disc_meeting_id):
    request.session['disc_meeting_id'] = disc_meeting_id
    disc_meeting = DiscplineMeeting.objects.get(id=disc_meeting_id)
    context = {
        "disc_meeting": disc_meeting,
        "id": disc_meeting_id
    }

    return render(request, 'hr_template/conclude_disc_meeting_view.html', context)


@login_required(login_url='user_login')
def conclude_disc_meeting_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        disc_meeting_id = request.session.get('disc_meeting_id')
        verdict = request.POST.get('verdict')
        disc_meeting = DiscplineMeeting.objects.get(id=disc_meeting_id)
        try:
            disc_meeting.verdict = verdict
            disc_meeting.status = True
            disc_meeting.save()

            del request.session['disc_meeting_id']
            messages.success(request, "Discpline Meeting Was Concluded Successfully!")
            return redirect('conclude_disc_meeting_view')
        except:
            messages.error(request, "Failed to Conclude Discpline Meeting.")
            return redirect('conclude_disc_meeting_view')


@login_required(login_url='user_login')
def concluded_disc_meeting_view(request):
    user = User.objects.get(id=request.user.id)
    hr = Human_resource_managers.objects.get(admin__user=user)
    office = hr.office
    disc_meetings = DiscplineMeeting.objects.filter(office=office, status=True)
    context = {
        "disc_meetings": disc_meetings
    }
    return render(request, 'hr_template/concluded_disc_meeting_view.html', context)


@csrf_exempt
def get_accussers(request):
    # Getting Values from Ajax POST 'Fetch Student'
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office

    acu_category = request.POST.get("acu_category")

    if acu_category == 'CEO':
        acu_names = CEO.objects.filter(office=office)
    elif acu_category == 'SWO':
        acu_names = Social_welfare_officers.objects.filter(office=office)
    elif acu_category == 'Accountant':
        acu_names = Accountant.objects.filter(office=office)
    elif acu_category == 'HR':
        acu_names = Human_resource_managers.objects.filter(office=office)
    elif acu_category == 'Lawyer':
        acu_names = Lawyers.objects.all()
    elif acu_category == 'Customer Service':
        acu_names = Customer_service.objects.filter(office=office)
    elif acu_category == 'Apartment Driver':
        acu_names = Drivers.objects.filter(office=office)
    elif acu_category == 'Apartment Admin':
        acu_names = AdminHOD.objects.filter(office=office)
    elif acu_category == 'Hotel Admin':
        acu_names = H_AdminHOD.objects.filter(office=office)
    else:
        acu_names = ""


    # Only Passing Student Id and Student Name Only
    list_data1 = []


    for acu_name in acu_names:
        data_small1={"id":acu_name.id, "acu_name":acu_name.admin.user.first_name+" "+acu_name.admin.user.last_name}
        list_data1.append(data_small1)

    return JsonResponse(json.dumps(list_data1), content_type="application/json", safe=False)


@csrf_exempt
def get_defendants(request):
    # Getting Values from Ajax POST 'Fetch Student'
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office

    def_category = request.POST.get("def_category")

    if def_category == 'CEO':
        def_names = CEO.objects.filter(office=office)
    elif def_category == 'SWO':
        def_names = Social_welfare_officers.objects.filter(office=office)
    elif def_category == 'Accountant':
        def_names = Accountant.objects.filter(office=office)
    elif def_category == 'HR':
        def_names = Human_resource_managers.objects.filter(office=office)
    elif def_category == 'Lawyer':
        def_names = Lawyers.objects.all()
    elif def_category == 'Customer Service':
        def_names = Customer_service.objects.filter(office=office)
    elif def_category == 'Apartment Driver':
        def_names = Drivers.objects.filter(office=office)
    elif def_category == 'Apartment Admin':
        def_names = AdminHOD.objects.filter(office=office)
    elif def_category == 'Hotel Admin':
        def_names = H_AdminHOD.objects.filter(office=office)
    else:
        def_names = ""


    # Only Passing Student Id and Student Name Only
    list_data2 = []


    for def_name in def_names:
        data_small2={"id":def_name.id, "def_name":def_name.admin.user.first_name+" "+def_name.admin.user.last_name}
        list_data2.append(data_small2)

    return JsonResponse(json.dumps(list_data2), content_type="application/json", safe=False)


@login_required(login_url='user_login')
def hr_cs_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = Human_resource_managers.objects.get(admin__user=user)
    office = admin_obj.office
    css = Customer_service.objects.filter(office=office)
    for cs in css:
        feedbacks = CSFeedBackHR.objects.filter(cs_id=cs)
        context = {
            "feedbacks": feedbacks
        }
        return render(request, 'hr_template/cs_feedback_template.html', context)


@csrf_exempt
def hr_cs_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = CSFeedBackHR.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def hr_swo_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = Human_resource_managers.objects.get(admin__user=user)
    office = admin_obj.office
    swos = Social_welfare_officers.objects.filter(office=office)
    for swo in swos:
        feedbacks = FeedBackSWO.objects.filter(swo_id=swo)
        context = {
            "feedbacks": feedbacks
        }
        return render(request, 'hr_template/swo_feedback_template.html', context)


@csrf_exempt
def hr_swo_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackSWO.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def hr_acc_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = Human_resource_managers.objects.get(admin__user=user)
    office = admin_obj.office
    accs = Accountant.objects.filter(office=office)
    for acc in accs:
        feedbacks = FeedBackAccountant.objects.filter(accountant_id=acc)
        context = {
            "feedbacks": feedbacks
        }
        return render(request, 'hr_template/acc_feedback_template.html', context)


@csrf_exempt
def hr_acc_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackAccountant.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def hr_h_admin_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = Human_resource_managers.objects.get(admin__user=user)
    office = admin_obj.office
    h_admins = H_AdminHOD.objects.filter(office=office)
    for h_admin in h_admins:
        feedbacks = FeedBackH_Admin.objects.filter(h_admin_id=h_admin)
        context = {
            "feedbacks": feedbacks
        }
        return render(request, 'hr_template/h_admin_feedback_template.html', context)


@csrf_exempt
def hr_h_admin_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackH_Admin.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def hr_admin_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = Human_resource_managers.objects.get(admin__user=user)
    office = admin_obj.office
    admins = AdminHOD.objects.filter(office=office)
    for admin in admins:
        feedbacks = FeedBackAdmin.objects.filter(admin_id=admin)
        context = {
            "feedbacks": feedbacks
        }
        return render(request, 'hr_template/admin_feedback_template.html', context)


@csrf_exempt
def hr_admin_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackAdmin.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def hr_lawyer_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    admin_obj = Human_resource_managers.objects.get(admin__user=user)
    office = admin_obj.office
    feedbacks = FeedBackLawyer.objects.filter(office=office).order_by('lawyer_id')
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hr_template/lawyer_feedback_template.html', context)


@csrf_exempt
def hr_lawyer_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackLawyer.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")
