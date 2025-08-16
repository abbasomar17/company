from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
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
from company.settings import BASE_DIR

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
def dc_home(request):
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
    no_dis_case = DiscplineMeeting.objects.all().count()
    no_dis_meeting = DiscplineMeeting.objects.filter(status=True).count()
    no_ceo_meetings = CEOMeeting.objects.all().count()
    no_hr_meetings = HRMeeting.objects.all().count()
    all_ceo_accept_leave_count = LeaveReportCEO.objects.filter(leave_status=1).count()
    all_ceo_reject_leave_count = LeaveReportCEO.objects.filter(leave_status=2).count()
    all_ceo_pending_leave_count = LeaveReportCEO.objects.filter(leave_status=0).count()
    all_ceo_accept_perm_count = PermissionReportCEO.objects.filter(leave_status=1).count()
    all_ceo_reject_perm_count = PermissionReportCEO.objects.filter(leave_status=2).count()
    all_ceo_pending_perm_count = PermissionReportCEO.objects.filter(leave_status=0).count()

    all_office_count = Office.objects.all().count()
    all_hr_count = Human_resource_managers.objects.all().count()
    all_swo_count = Social_welfare_officers.objects.all().count()
    all_lawyer_count = Lawyers.objects.all().count()
    all_accountant_count = Accountant.objects.all().count()
    all_admin_count = AdminHOD.objects.all().count()
    all_h_admin_count = H_AdminHOD.objects.all().count()
    all_cs_count = Customer_service.objects.all().count()
    all_ceo_count = CEO.objects.all().count()
    total_staff = all_cs_count + all_h_admin_count + all_admin_count + all_hr_count + all_lawyer_count + all_accountant_count + all_swo_count + all_ceo_count

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

    if Office.objects.all().exists():
        office_law_sal = law_sal_year / all_office_count
    else:
        office_law_sal = 0


    office_all = Office.objects.all()
    office_names_list = []
    hr_count_list_in_office = []
    swo_count_list_in_office = []
    accountant_count_list_in_office = []
    cs_count_list_in_office = []
    admin_count_list_in_office = []
    h_admin_count_list_in_office = []
    ceo_count_list_in_office = []

    hr_salaries_list_in_office = []
    swo_salaries_list_in_office = []
    accountant_salaries_list_in_office = []
    cs_salaries_list_in_office = []
    admin_salaries_list_in_office = []
    h_admin_salaries_list_in_office = []
    ceo_salaries_list_in_office = []

    total_salaries_list_in_office = []
    overdue_list_in_office = []
    income_list_in_office = []
    total_expenditure_list_in_office = []
    h_payment_list_in_office = []
    a_payment_list_in_office = []
    total_income_list_in_office = []

    overdue_count_list_in_office = []
    income_count_list_in_office = []
    h_payment_count_list_in_office = []
    a_payment_count_list_in_office = []
    income_expenditure_list_in_office = []

    ceo_pending_leaves_list_in_office = []
    ceo_pending_perms_list_in_office = []
    ceo_accept_leaves_list_in_office = []
    ceo_accept_perms_list_in_office = []
    ceo_reject_leaves_list_in_office = []
    ceo_reject_perms_list_in_office = []

    dis_meeting_list_in_office = []
    dis_case_list_in_office = []
    dis_ratio_list_in_office = []

    ceo_meeting_list_in_office = []
    hr_meeting_list_in_office = []
    total_meeting_list_in_office = []

    for office in office_all:
        no_ceo_meetings_office = CEOMeeting.objects.filter(office=office).count()
        no_hr_meetings_office = HRMeeting.objects.filter(office=office).count()
        total_meetings = no_hr_meetings_office + no_ceo_meetings_office
        no_dis_case_office = DiscplineMeeting.objects.filter(office=office).count()
        no_dis_meeting_office = DiscplineMeeting.objects.filter(status=True, office=office).count()
        if DiscplineMeeting.objects.filter(office=office).exists():
            dis_ratio = no_dis_meeting_office/no_dis_case_office
        else:
            dis_ratio = 0
        if CEO.objects.filter(office=office).exists():
            office_ceo_accept_leave_count = LeaveReportCEO.objects.filter(leave_status=1, ceo_id__office=office).count()
            office_ceo_reject_leave_count = LeaveReportCEO.objects.filter(leave_status=2, ceo_id__office=office).count()
            office_ceo_pending_leave_count = LeaveReportCEO.objects.filter(leave_status=0, ceo_id__office=office).count()
            office_ceo_accept_perm_count = PermissionReportCEO.objects.filter(leave_status=1, ceo_id__office=office).count()
            office_ceo_reject_perm_count = PermissionReportCEO.objects.filter(leave_status=2, ceo_id__office=office).count()
            office_ceo_pending_perm_count = PermissionReportCEO.objects.filter(leave_status=0, ceo_id__office=office).count()
        else:
            office_ceo_accept_leave_count = 0
            office_ceo_reject_leave_count = 0
            office_ceo_pending_leave_count = 0
            office_ceo_accept_perm_count = 0
            office_ceo_reject_perm_count = 0
            office_ceo_pending_perm_count = 0

        if SalaryCEO.objects.filter(office=office).exists() and CEO.objects.filter(office=office).exists():
            office_ceo_count = CEO.objects.filter(office=office).count()
            office_ceo = CEO.objects.get(office=office)
            employed = office_ceo.created_at.year
            t = int((year - employed) / 3)
            no_salary = SalaryCEO.objects.filter(office=office).first()
            new_salary = no_salary.amount * (pow((1 + rate), t))
            ceo_salary = round((ceo_salary + new_salary), 2)
            ceo_sal_year = ceo_salary * 12
        else:
            office_ceo_count = 0
            ceo_sal_year = 0

        if SalaryHR.objects.filter(office=office).exists() and Human_resource_managers.objects.filter(office=office).exists():
            office_hrs = Human_resource_managers.objects.filter(office=office)
            office_hrs_count = Human_resource_managers.objects.filter(office=office).count()
            for hr in office_hrs:
                employed = hr.created_at.year
                t = int((year - employed) / 3)
                no_salary = SalaryHR.objects.filter(office=office).first()
                new_salary = no_salary.amount * (pow((1 + rate), t))
                hr_salary = round((hr_salary + new_salary), 2)
            hr_sal_year = hr_salary * 12
        else:
            hr_sal_year = 0
            office_hrs_count = 0

        if SalarySWO.objects.filter(office=office).exists() and Social_welfare_officers.objects.filter(office=office).exists():
            office_swos = Social_welfare_officers.objects.filter(office=office)
            office_swos_count = Social_welfare_officers.objects.filter(office=office).count()
            for swo in office_swos:
                employed = swo.created_at.year
                t = (year - employed) / 3
                no_salary = SalarySWO.objects.filter(office=office).first()
                new_salary = no_salary.amount * (pow((1 + rate), t))
                swo_salary = swo_salary + new_salary
            swo_sal_year = swo_salary * 12
        else:
            swo_sal_year = 0
            office_swos_count = 0

        if SalaryAccountant.objects.filter(office=office).exists() and Accountant.objects.filter(office=office).exists():
            office_accs = Accountant.objects.filter(office=office)
            office_accs_count = Accountant.objects.filter(office=office).count()
            for acc in office_accs:
                employed = acc.created_at.year
                t = int((year - employed) / 3)
                no_salary = SalaryAccountant.objects.filter(office=office).first()
                new_salary = no_salary.amount * (pow((1 + rate), t))
                acc_salary = round((acc_salary + new_salary), 2)
            acc_sal_year = acc_salary * 12
        else:
            acc_sal_year = 0
            office_accs_count = 0

        if SalaryAdmin.objects.filter(office=office).exists() and H_AdminHOD.objects.filter(office=office).exists():
            office_h_admin = H_AdminHOD.objects.filter(office=office)
            office_h_admin_count = H_AdminHOD.objects.filter(office=office).count()
            for h_admin in office_h_admin:
                employed = h_admin.created_at.year
                t = int((year - employed) / 3)
                no_salary = SalaryAdmin.objects.filter(office=office).first()
                new_salary = no_salary.amount * (pow((1 + rate), t))
                h_admin_salary = round((h_admin_salary + new_salary),2)
            h_admin_sal_year = h_admin_salary * 12
        else:
            h_admin_sal_year = 0
            office_h_admin_count = 0

        if SalaryAdmin.objects.filter(office=office).exists() and AdminHOD.objects.filter(office=office).exists():
            office_admin = AdminHOD.objects.filter(office=office)
            office_admin_count = AdminHOD.objects.filter(office=office).count()
            for admin in office_admin:
                employed = admin.created_at.year
                t = int((year - employed) / 3)
                no_salary = SalaryAdmin.objects.filter(office=office).first()
                new_salary = no_salary.amount * (pow((1 + rate), t))
                admin_salary = round((admin_salary + new_salary),2)
            admin_sal_year = admin_salary * 12
        else:
            admin_sal_year = 0
            office_admin_count = 0

        if SalaryCS.objects.filter(office=office).exists() and Customer_service.objects.filter(office=office).exists():
            office_css = Customer_service.objects.filter(office=office)
            office_css_count = Customer_service.objects.filter(office=office).count()
            for cs in office_css:
                employed = cs.created_at.year
                t = int((year - employed) / 3)
                no_salary = SalaryCS.objects.filter(office=office).first()
                new_salary = no_salary.amount * (pow((1 + rate), t))
                cs_salary = round((cs_salary + new_salary),2)
            cs_sal_year = cs_salary * 12
        else:
            cs_sal_year = 0
            office_css_count = 0

        total_salary = ceo_sal_year + cs_sal_year + admin_sal_year + h_admin_sal_year + office_law_sal + hr_sal_year + acc_sal_year + swo_sal_year

        office_overdue = Overdue.objects.filter(office=office)
        office_overdue_count = Overdue.objects.filter(office=office).count()
        for overdue in office_overdue:
            amount = overdue.amount
            overdue_cost = overdue_cost + amount

        total_expenditure = total_salary + overdue_cost

        office_a_p = ApartmentPayment.objects.filter(office=office)
        office_a_p_count = ApartmentPayment.objects.filter(office=office).count()
        for a_p in office_a_p:
            amount = a_p.amount
            a_payment = a_payment + amount

        office_income = Incomes.objects.filter(office=office)
        office_income_count = Incomes.objects.filter(office=office).count()
        for income in office_income:
            amount = income.amount
            o_income = o_income + amount

        total_income = h_payment + o_income + a_payment
        if total_expenditure != 0:
            ratio_income_expenditure = total_income/total_expenditure
        else:
            ratio_income_expenditure = 0

        office_names_list.append(office.title)
        hr_count_list_in_office.append(office_hrs_count)
        swo_count_list_in_office.append(office_swos_count)
        accountant_count_list_in_office.append(office_accs_count)
        cs_count_list_in_office.append(office_css_count)
        ceo_count_list_in_office.append(office_ceo_count)
        admin_count_list_in_office.append(office_admin_count)
        h_admin_count_list_in_office .append(office_h_admin_count)
        hr_salaries_list_in_office.append(hr_sal_year)
        swo_salaries_list_in_office.append(swo_sal_year)
        accountant_salaries_list_in_office.append(acc_sal_year)
        cs_salaries_list_in_office.append(cs_sal_year)
        admin_salaries_list_in_office.append(admin_sal_year)
        h_admin_salaries_list_in_office.append(h_admin_sal_year)
        ceo_salaries_list_in_office.append(ceo_sal_year)
        total_salaries_list_in_office.append(total_salary)
        overdue_list_in_office.append(overdue_cost)
        income_list_in_office.append(o_income)
        total_expenditure_list_in_office.append(total_expenditure)
        h_payment_list_in_office.append(h_payment)
        a_payment_list_in_office.append(a_payment)
        total_income_list_in_office.append(total_income)
        overdue_count_list_in_office.append(office_overdue_count)
        income_count_list_in_office.append(office_income_count)
        a_payment_count_list_in_office.append(office_a_p_count)
        income_expenditure_list_in_office.append(ratio_income_expenditure)
        ceo_accept_leaves_list_in_office.append(office_ceo_accept_leave_count)
        ceo_reject_leaves_list_in_office.append(office_ceo_reject_leave_count)
        ceo_pending_leaves_list_in_office.append(office_ceo_pending_leave_count)
        ceo_accept_perms_list_in_office.append(office_ceo_accept_perm_count)
        ceo_reject_perms_list_in_office.append(office_ceo_reject_perm_count)
        ceo_pending_perms_list_in_office.append(office_ceo_pending_perm_count)
        dis_meeting_list_in_office.append(no_dis_meeting_office)
        dis_case_list_in_office.append(no_dis_case_office)
        dis_ratio_list_in_office.append(dis_ratio)
        ceo_meeting_list_in_office.append(no_ceo_meetings_office)
        hr_meeting_list_in_office.append(no_hr_meetings_office)
        total_meeting_list_in_office.append(total_meetings)

    hr_count_list_in_all = sum(hr_count_list_in_office)
    swo_count_list_in_all = sum(swo_count_list_in_office)
    accountant_count_list_in_all = sum(accountant_count_list_in_office)
    cs_count_list_in_all = sum(cs_count_list_in_office)
    admin_count_list_in_all = sum(admin_count_list_in_office)
    h_admin_count_list_in_all = sum(h_admin_count_list_in_office)

    hr_salaries_list_in_all = sum(hr_salaries_list_in_office)
    swo_salaries_list_in_all = sum(swo_salaries_list_in_office)
    accountant_salaries_list_in_all = sum(accountant_salaries_list_in_office)
    cs_salaries_list_in_all = sum(cs_salaries_list_in_office)
    admin_salaries_list_in_all = sum(admin_salaries_list_in_office)
    h_admin_salaries_list_in_all = sum(h_admin_salaries_list_in_office)
    ceo_salaries_list_in_all = sum(ceo_salaries_list_in_office)

    total_salaries_list_in_all = sum(total_salaries_list_in_office)
    overdue_list_in_all = sum(overdue_list_in_office)
    income_list_in_all = sum(income_list_in_office)
    total_expenditure_list_in_all = sum(total_expenditure_list_in_office)
    h_payment_list_in_all = sum(h_payment_list_in_office)
    a_payment_list_in_all = sum(a_payment_list_in_office)
    total_income_list_in_all = sum(total_income_list_in_office)

    overdue_count_list_in_all = sum(overdue_count_list_in_office)
    income_count_list_in_all = sum(income_count_list_in_office)
    h_payment_count_list_in_all = sum(h_payment_count_list_in_office)
    a_payment_count_list_in_all = sum(a_payment_count_list_in_office)
    if Office.objects.all().exists():
        income_expenditure_list_in_all = (sum(income_expenditure_list_in_office)) / all_office_count
    else:
        income_expenditure_list_in_all = 0

    context = {
        "total_staff": total_staff,
        "rate": rate,
        "office_names_list": office_names_list,
        "hr_count_list_in_office": hr_count_list_in_office,
        "swo_count_list_in_office": swo_count_list_in_office,
        "accountant_count_list_in_office": accountant_count_list_in_office,
        "cs_count_list_in_office": cs_count_list_in_office,
        "ceo_count_list_in_office": ceo_count_list_in_office,
        "admin_count_list_in_office": admin_count_list_in_office,
        "h_admin_count_list_in_office": h_admin_count_list_in_office,
        "office_law_sal": office_law_sal,
        "law_sal_year": law_sal_year,
        "hr_salaries_list_in_office": hr_salaries_list_in_office,
        "swo_salaries_list_in_office": swo_salaries_list_in_office,
        "accountant_salaries_list_in_office": accountant_salaries_list_in_office,
        "cs_salaries_list_in_office": cs_salaries_list_in_office,
        "admin_salaries_list_in_office": admin_salaries_list_in_office,
        "h_admin_salaries_list_in_office": h_admin_salaries_list_in_office,
        "ceo_salaries_list_in_office": ceo_salaries_list_in_office,
        "total_salaries_list_in_office": total_salaries_list_in_office,
        "overdue_list_in_office": overdue_list_in_office,
        "income_list_in_office": income_list_in_office,
        "total_expenditure_list_in_office": total_expenditure_list_in_office,
        "h_payment_list_in_office": h_payment_list_in_office,
        "a_payment_list_in_office": a_payment_list_in_office,
        "total_income_list_in_office": total_income_list_in_office,
        "overdue_count_list_in_office": overdue_count_list_in_office,
        "income_count_list_in_office": income_count_list_in_office,
        "h_payment_count_list_in_office": h_payment_count_list_in_office,
        "a_payment_count_list_in_office": a_payment_count_list_in_office,
        "income_expenditure_list_in_office": income_expenditure_list_in_office,
        "hr_count_list_in_all": hr_count_list_in_all,
        "swo_count_list_in_all": swo_count_list_in_all,
        "accountant_count_list_in_all": accountant_count_list_in_all,
        "cs_count_list_in_all": cs_count_list_in_all,
        "admin_count_list_in_all": admin_count_list_in_all,
        "h_admin_count_list_in_all": h_admin_count_list_in_all,
        "hr_salaries_list_in_all": hr_salaries_list_in_all,
        "swo_salaries_list_in_all": swo_salaries_list_in_all,
        "accountant_salaries_list_in_all": accountant_salaries_list_in_all,
        "cs_salaries_list_in_all": cs_salaries_list_in_all,
        "admin_salaries_list_in_all": admin_salaries_list_in_all,
        "h_admin_salaries_list_in_all": h_admin_salaries_list_in_all,
        "ceo_salaries_list_in_all": ceo_salaries_list_in_all,
        "total_salaries_list_in_all": total_salaries_list_in_all,
        "overdue_list_in_all": overdue_list_in_all,
        "income_list_in_all": income_list_in_all,
        "total_expenditure_list_in_all": total_expenditure_list_in_all,
        "h_payment_list_in_all": h_payment_list_in_all,
        "a_payment_list_in_all": a_payment_list_in_all,
        "total_income_list_in_all": total_income_list_in_all,
        "overdue_count_list_in_all": overdue_count_list_in_all,
        "income_count_list_in_all": income_count_list_in_all,
        "h_payment_count_list_in_all": h_payment_count_list_in_all,
        "a_payment_count_list_in_all": a_payment_count_list_in_all,
        "income_expenditure_list_in_all": income_expenditure_list_in_all,
        "ceo_pending_leaves_list_in_office": ceo_pending_leaves_list_in_office,
        "ceo_pending_perms_list_in_office": ceo_pending_perms_list_in_office,
        "ceo_accept_leaves_list_in_office": ceo_accept_leaves_list_in_office,
        "ceo_accept_perms_list_in_office": ceo_accept_perms_list_in_office,
        "ceo_reject_leaves_list_in_office": ceo_reject_leaves_list_in_office,
        "ceo_reject_perms_list_in_office": ceo_reject_perms_list_in_office,
        "dis_meeting_list_in_office": dis_meeting_list_in_office,
        "dis_case_list_in_office": dis_case_list_in_office,
        "dis_ratio_list_in_office": dis_ratio_list_in_office,
        "ceo_meeting_list_in_office": ceo_meeting_list_in_office,
        "hr_meeting_list_in_office": hr_meeting_list_in_office,
        "total_meeting_list_in_office": total_meeting_list_in_office,
        "no_hr_meetings": no_hr_meetings,
        "no_ceo_meetings": no_ceo_meetings,
        "all_cs_count": all_cs_count,
        "all_ceo_count": all_ceo_count,
        "all_h_admin_count": all_h_admin_count,
        "all_admin_count": all_admin_count,
        "all_accountant_count": all_accountant_count,
        "all_office_count": all_office_count,
        "all_lawyer_count": all_lawyer_count,
        "no_dis_case": no_dis_case,
        "no_dis_meeting": no_dis_meeting,
        "all_swo_count": all_swo_count,
        "all_hr_count": all_hr_count,
        "all_ceo_accept_leave_count": all_ceo_accept_leave_count,
        "all_ceo_reject_leave_count": all_ceo_reject_leave_count,
        "all_ceo_pending_leave_count": all_ceo_pending_leave_count,
        "all_ceo_accept_perm_count": all_ceo_accept_perm_count,
        "all_ceo_reject_perm_count": all_ceo_reject_perm_count,
        "all_ceo_pending_perm_count": all_ceo_pending_perm_count,
    }
    return render(request, "dc_template/home_content.html", context)


@login_required(login_url='user_login')
def add_rate(request):
    form = AddRateForm()
    context = {
        "form": form
    }
    return render(request, 'dc_template/add_rate_template.html', context)


@login_required(login_url='user_login')
def add_rate_save(request):
    if request.method == "POST":
        form = AddRateForm(request.POST)
        if form.is_valid():
            rate = form.cleaned_data['rate']


            rate = Rate(rate=rate)
            rate.save()
            messages.success(request, "Increment Added Successfully!")
            return redirect('add_rate')
    else:
        form = AddRateForm()
        context = {
            'form': form
        }
        return render(request, 'dc_template/add_rate_template.html', context)


@login_required(login_url='user_login')
def manage_rate(request):
    rates = Rate.objects.all()
    context = {
        "rates": rates
    }
    return render(request, 'dc_template/manage_rate_template.html', context)


@login_required(login_url='user_login')
def edit_rate(request, rate_id):
    # Adding Student ID into Session Variable
    request.session['rate_id'] = rate_id

    obj = Rate.objects.get(id=rate_id)
    form = EditRateForm()
    # Filling the form with Data from Database
    form.fields['rate'].initial = obj.rate

    context = {
        "rate_id": rate_id,
        "username": obj.rate,
        "form": form
    }
    return render(request, "dc_template/edit_rate_template.html", context)


@login_required(login_url='user_login')
def rate_edit(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        rate_id = request.session.get('rate_id')
        if rate_id == None:
            return redirect('manage_rate')

        form = EditRateForm(request.POST)
        if form.is_valid():
            rate = form.cleaned_data['rate']


            try:
                # First Update into Custom User Model
                obj = Rate.objects.get(id=rate_id)
                obj.rate = rate

                obj.save()
                # Delete student_id SESSION after the data is updated
                del request.session['rate_id']

                messages.success(request, "Increment Updated Successfully!")
                return redirect('/edit_rate/'+rate_id)
            except:
                messages.success(request, "Failed to Update Increment.")
                return redirect('/edit_rate/'+rate_id)
        else:
            return redirect('/edit_rate'+rate_id)


@login_required(login_url='user_login')
def delete_rate(request, rate_id):
    rate = Rate.objects.get(id=rate_id)
    try:
        rate.delete()
        messages.success(request, "Increment Deleted Successfully.")
        return redirect('manage_rate')
    except:
        messages.error(request, "Failed to Delete Increment.")
        return redirect('manage_rate')


@login_required(login_url='user_login')
def add_office(request):
    form = AddOfficeForm()
    context = {
        "form": form
    }
    return render(request, 'dc_template/add_office_template.html', context)


@login_required(login_url='user_login')
def add_office_save(request):
    if request.method == "POST":
        office_form = AddOfficeForm(request.POST)
        if office_form.is_valid():
            title = office_form.cleaned_data['title']
            region = office_form.cleaned_data['region']
            town = office_form.cleaned_data['town']
            spec_location = office_form.cleaned_data['spec_location']
            address = office_form.cleaned_data['address']


            office = Office(title=title, region=region, town=town, spec_location=spec_location, address=address)
            office.save()
            messages.success(request, "Office Added Successfully!")
            return redirect('add_office')
    else:
        office_form = AddOfficeForm()
        context = {
            'office_form': office_form
        }
        return render(request, 'dc_template/add_office_template.html', context)


@login_required(login_url='user_login')
def manage_office(request):
    offices = Office.objects.all()
    context = {
        "offices": offices
    }
    return render(request, 'dc_template/manage_office_template.html', context)


@login_required(login_url='user_login')
def edit_office(request, office_id):
    # Adding Student ID into Session Variable
    request.session['office_id'] = office_id

    office = Office.objects.get(id=office_id)
    form = EditOfficeForm()
    # Filling the form with Data from Database
    form.fields['title'].initial = office.title
    form.fields['spec_location'].initial = office.spec_location
    form.fields['region'].initial = office.region
    form.fields['town'].initial = office.town
    form.fields['address'].initial = office.address

    context = {
        "id": office_id,
        "username": office.title,
        "form": form
    }
    return render(request, "dc_template/edit_office_template.html", context)


@login_required(login_url='user_login')
def edit_office_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        office_id = request.session.get('office_id')
        if office_id == None:
            return redirect('manage_office')

        form = EditOfficeForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            spec_location = form.cleaned_data['spec_location']
            town = form.cleaned_data['town']
            region = form.cleaned_data['region']
            address = form.cleaned_data['address']


            try:
                # First Update into Custom User Model
                office = Office.objects.get(id=office_id)
                office.title = title
                office.spec_location = spec_location
                office.region = region
                office.town = town
                office.address = address

                office.save()
                # Delete student_id SESSION after the data is updated
                del request.session['office_id']

                messages.success(request, "Office Updated Successfully!")
                return redirect('/edit_office/'+office_id)
            except:
                messages.success(request, "Failed to Update Office.")
                return redirect('/edit_office/'+office_id)
        else:
            return redirect('/edit_office/'+office_id)


@login_required(login_url='user_login')
def delete_office(request, office_id):
    office = Office.objects.get(id=office_id)
    try:
        office.delete()
        messages.success(request, "Office Deleted Successfully.")
        return redirect('manage_office')
    except:
        messages.error(request, "Failed to Delete Office.")
        return redirect('manage_office')


@login_required(login_url='user_login')
def add_ceo(request):
    offices = Office.objects.all()
    contexts = {
        "offices": offices
    }
    return render(request, 'dc_template/add_ceo_template.html', contexts)


@login_required(login_url='user_login')
def add_ceo_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_ceo')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        nida_number = request.POST.get('nida_number')

        office_id = request.POST.get('office')
        try:

            office_obj = Office.objects.get(id=office_id)

            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type = 1)
            customer.save()

            ceo = CEO(admin=customer, office=office_obj, address=address, nida_number=nida_number)
            ceo.save()
            messages.success(request, "CEO Added Successfully!")
            return redirect('add_ceo')
        except:
            messages.success(request, "Failed to add CEO!")
            return render(request, 'dc_template/add_ceo_template.html')


@login_required(login_url='user_login')
def manage_ceo(request):
    ceos = CEO.objects.all()
    context = {
        "ceos": ceos
    }
    return render(request, 'dc_template/manage_ceo_template.html', context)


@login_required(login_url='user_login')
def edit_ceo(request, ceo_id):
    # Adding Student ID into Session Variable

    request.session['salary_ceo_id'] = ceo_id
    offices = Office.objects.all()
    ceo = CEO.objects.get(id=ceo_id)
    context = {
        "offices": offices,
        "ceo": ceo,
        "id": ceo_id
    }
    return render(request, "dc_template/edit_ceo_template.html", context)


@login_required(login_url='user_login')
def edit_ceo_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        ceo_id = request.session.get('ceo_id')
        if ceo_id == None:
            return redirect('manage_ceo')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')

        office = request.POST.get('office')

        try:
            # First Update into Custom User Model
            user = CEO.objects.get(id=ceo_id)
            user.admin.user.first_name = first_name
            user.admin.user.last_name = last_name
            user.admin.user.email = email
            user.admin.user.username = username
            user.admin.user.password = password


            # Then Update Students Table

            user.address = address

            office = Office.objects.get(id=office)
            user.office = office

            user.save()
            # Delete student_id SESSION after the data is updated
            del request.session['ceo_id']

            messages.success(request, "CEO Updated Successfully!")
            return redirect('/edit_ceo/'+ceo_id)
        except:
            messages.success(request, "Failed to Update CEO.")
            return redirect('/edit_ceo/'+ceo_id)



@login_required(login_url='user_login')
def delete_ceo(request, ceo_id):
    ceo = CEO.objects.get(id=ceo_id)
    try:
        ceo.delete()
        messages.success(request, "CEO Deleted Successfully.")
        return redirect('manage_ceo')
    except:
        messages.error(request, "Failed to Delete CEO.")
        return redirect('manage_ceo')


@login_required(login_url='user_login')
def add_resp_ceo(request):
    return render(request, "dc_template/add_resp_ceo_template.html")


@login_required(login_url='user_login')
def add_resp_ceo_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_resp_ceo')
    else:
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_ceo_model = ResponsibilityCEO(name=name, description=description)
            resp_ceo_model.save()
            messages.success(request, "Conduct CEO Responsibility Added Successfully!")
            return redirect('add_resp_ceo')
        except:
            messages.error(request, "Failed to Add CEO Responsibility!")
            return redirect('add_resp_ceo')


@login_required(login_url='user_login')
def manage_resp_ceo(request):
    resp_ceos = ResponsibilityCEO.objects.all()
    context = {
        "resp_ceos": resp_ceos
    }
    return render(request, 'dc_template/manage_resp_ceo_template.html', context)


@login_required(login_url='user_login')
def edit_resp_ceo(request, resp_ceo_id):
    request.session['resp_ceo_id'] = resp_ceo_id
    resp_ceo = ResponsibilityCEO.objects.get(id=resp_ceo_id)
    context = {
        "resp_ceo": resp_ceo,
        "id": resp_ceo_id,
    }
    return render(request, 'dc_template/edit_resp_ceo_template.html', context)


@login_required(login_url='user_login')
def edit_resp_ceo_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        resp_ceo_id = request.session.get('resp_ceo_id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_ceo = ResponsibilityCEO.objects.get(id=resp_ceo_id)
            resp_ceo.name = name
            resp_ceo.description = description
            resp_ceo.save()

            messages.success(request, "CEO Responsibility Updated Successfully.")
            return redirect('/edit_resp_ceo/'+resp_ceo_id)

        except:
            messages.error(request, "Failed to Update CEO Responsibility.")
            return redirect('/edit_resp_ceo/'+resp_ceo_id)


@login_required(login_url='user_login')
def delete_resp_ceo(request, resp_ceo_id):
    resp_ceo = ResponsibilityCEO.objects.get(id=resp_ceo_id)
    try:
        resp_ceo.delete()
        messages.success(request, "CEO Responsibility Deleted Successfully.")
        return redirect('manage_resp_ceo')
    except:
        messages.error(request, "Failed to Delete CEO Responsibility.")
        return redirect('manage_resp_ceo')


@login_required(login_url='user_login')
def add_salary_ceo(request):
    offices = Office.objects.all()
    contexts = {
        "offices": offices
    }
    return render(request, "dc_template/add_salary_ceo_template.html", contexts)


@login_required(login_url='user_login')
def add_salary_ceo_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_ceo')
    else:
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        office_id = request.POST.get('office')
        office = Office.objects.get(id=office_id)
        try:
            salary_ceo_model = SalaryCEO(amount=amount, office=office, description=description)
            salary_ceo_model.save()
            messages.success(request, "CEO Salary Added Successfully!")
            return redirect('add_salary_ceo')
        except:
            messages.error(request, "Failed to Add CEO Salary!")
            return redirect('add_salary_ceo')


@login_required(login_url='user_login')
def manage_salary_ceo(request):
    salary_ceos = SalaryCEO.objects.all()
    context = {
        "salary_ceos": salary_ceos
    }
    return render(request, 'dc_template/manage_salary_ceo_template.html', context)


@login_required(login_url='user_login')
def edit_salary_ceo(request, salary_ceo_id):
    request.session['salary_ceo_id'] = salary_ceo_id
    offices = Office.objects.all()
    salary_ceo = SalaryCEO.objects.get(id=salary_ceo_id)
    context = {
        "offices": offices,
        "salary_ceo": salary_ceo,
        "id": salary_ceo_id
    }
    return render(request, 'dc_template/edit_salary_ceo_template.html', context)


@login_required(login_url='user_login')
def edit_salary_ceo_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        salary_ceo_id = request.session.get('salary_ceo_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        office_id = request.POST.get('office')
        office = Office.objects.get(id=office_id)

        try:
            salary_ceo = SalaryCEO.objects.get(id=salary_ceo_id)
            salary_ceo.amount = amount
            salary_ceo.office = office
            salary_ceo.description = description
            salary_ceo.save()

            messages.success(request, "CEO Salary Updated Successfully.")
            return redirect('/edit_salary_ceo/'+salary_ceo_id)

        except:
            messages.error(request, "Failed to Update CEO Salary.")
            return redirect('/edit_salary_ceo/'+salary_ceo_id)


@login_required(login_url='user_login')
def delete_salary_ceo(request, salary_ceo_id):
    salary_ceo = SalaryCEO.objects.get(id=salary_ceo_id)
    try:
        salary_ceo.delete()
        messages.success(request, "CEO Salary Deleted Successfully.")
        return redirect('manage_salary_ceo')
    except:
        messages.error(request, "Failed to Delete CEO Salary.")
        return redirect('manage_salary_ceo')


@login_required(login_url='user_login')
def ceo_feedback_message(request):
    feedbacks = FeedBackCEO.objects.all().order_by('ceo_id')
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'dc_template/ceo_feedback_template.html', context)


@csrf_exempt
def ceo_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackCEO.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def add_notification_ceo(request):
    ceos = CEO.objects.all()
    context = {
        "ceos": ceos
    }
    return render(request, 'dc_template/add_ceo_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_ceo_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_ceo')
    else:
        message = request.POST.get('message')

        ceo_id = request.POST.get('ceo')
        ceo = CEO.objects.get(id=ceo_id)

        try:
            ceo_notification = NotificationCEO(message=message, ceo_id=ceo)
            ceo_notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_ceo')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_ceo')


@login_required(login_url='user_login')
def manage_notification_ceo(request):
    notifications = NotificationCEO.objects.all().order_by('ceo_id')
    context = {
        "notifications": notifications
    }
    return render(request, 'dc_template/manage_ceo_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_ceo(request, ceo_id):
    request.session['ceo_id'] = ceo_id

    ceo = CEO.objects.get(id=ceo_id)
    context = {
        "ceo": ceo,
        "id": ceo_id
    }
    return render(request, 'dc_template/edit_ceo_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_ceo_save(request):
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
def delete_notification_ceo(request, notification_ceo_id):
    notification_ceo = NotificationCEO.objects.get(id=notification_ceo_id)
    try:
        notification_ceo.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_ceo')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_ceo')


@login_required(login_url='user_login')
def dc_ceo_leave_view(request):
    leaves = LeaveReportCEO.objects.all().order_by('ceo_id')
    context = {
        "leaves": leaves
    }
    return render(request, 'dc_template/ceo_leave_view.html', context)


@login_required(login_url='user_login')
def dc_ceo_permission_view(request):
    permissions = PermissionReportCEO.objects.all().order_by('ceo_id')
    context = {
        "permissions": permissions
    }
    return render(request, 'dc_template/ceo_permission_view.html', context)


def user_login(request):
    return render(request, "dc_template/user_login_template.html")


def user_add_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('user_add')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_model = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user_model.save()
            custom = S_CustomUser(user=user_model, user_type=9)
            custom.save()
            messages.success(request, "User Added Successfully!")
            return redirect('user_login')
        except:
            messages.error(request, "Failed to Add User!")
            return redirect('user_add')


def user_add(request):
    return render(request, "dc_template/verify_user.html")


def verify_user(request):
    if request.method == "POST":
        code = request.POST.get('code')
        if code == "Abbas@17oa#1974":
            return render(request, "dc_template/user_add_template.html")
        else:
            return redirect('user_login')


@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('user_login')


def user_do_login(request):
    if request.method == "POST":
        if User.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            user = User.objects.get(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                custom = S_CustomUser.objects.get(user=user)
                user_type = custom.user_type
                # return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
                if user_type == '9':
                    return redirect('dc_home')
                elif user_type == '1':
                    # return HttpResponse("Staff Login")
                    return redirect('ceo_home')

                elif user_type == '2':
                    # return HttpResponse("Student Login")
                    return redirect('hr_home')
                elif user_type == '3':
                    return redirect('swo_home')
                elif user_type == '4':
                    return redirect("law_home")
                elif user_type == '5':
                    # return HttpResponse("Staff Login")
                    return redirect('cs_home')

                elif user_type == '6':
                    # return HttpResponse("Student Login")
                    return redirect('acc_home')
                elif user_type == '7':
                    return redirect('h_admin_home')
                elif user_type == '8':
                    return redirect("admin_home")
                else:
                    return redirect('user_login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            # return HttpResponseRedirect("/")
            return redirect('user_login')


@login_required(login_url='user_login')
def dc_profile(request):
    user = User.objects.get(id=request.user.id)
    custom_obj = S_CustomUser.objects.get(user=user)
    context= {
        "user": user,
        "custom": custom_obj,
    }
    return render(request, 'dc_template/dc_profile.html', context)


@login_required(login_url='user_login')
def dc_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('dc_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(id=request.user.id)
            customuser = S_CustomUser.objects.get(user=user)
            customuser.user.first_name = first_name
            customuser.user.last_name = last_name
            customuser.user.email = email
            customuser.user.username = username
            if password != None and password != "":
                customuser.user.set_password(password)
            customuser.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('dc_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('dc_profile')

