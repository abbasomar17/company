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
from .forms import *


@login_required(login_url='user_login')
def ceo_home(request):
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
    ceo_obj = CEO.objects.get(admin__user=user)
    hr_obj = S_CustomUser.objects.get(user=user)
    office = ceo_obj.office
    no_dis_case = DiscplineMeeting.objects.filter(office=office).count()
    no_dis_meeting = DiscplineMeeting.objects.filter(office=office, status=True).count()
    total_ceo_attendance = AttendanceCEOReport.objects.filter(attendant_id=hr_obj).count()
    attendance_ceo_present = AttendanceCEOReport.objects.filter(attendant_id=hr_obj, status=1).count()
    attendance_ceo_absent = AttendanceCEOReport.objects.filter(attendant_id=hr_obj, status=2).count()
    total_hr_attendance = AttendanceHRReport.objects.filter(attendant_id=hr_obj).count()
    attendance_hr_present = AttendanceHRReport.objects.filter(attendant_id=hr_obj, status=1).count()
    attendance_hr_absent = AttendanceHRReport.objects.filter(attendant_id=hr_obj, status=2).count()
    no_ceo_meetings = CEOMeeting.objects.filter(office=office).count()
    no_hr_meetings = HRMeeting.objects.filter(office=office).count()

    all_office_count = Office.objects.all().count()
    all_hr_count = Human_resource_managers.objects.filter(office=office).count()
    all_swo_count = Social_welfare_officers.objects.filter(office=office).count()
    all_lawyer_count = Lawyers.objects.all().count()
    all_accountant_count = Accountant.objects.filter(office=office).count()
    all_admin_count = AdminHOD.objects.filter(office=office).count()
    all_h_admin_count = H_AdminHOD.objects.filter(office=office).count()
    all_cs_count = Customer_service.objects.filter(office=office).count()
    all_ceo_count = CEO.objects.filter(office=office).count()
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
            no_salary = SalaryHR.objects.filter(office=office).first
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

    total_income = o_income + a_payment

    # Total Subjects and students in Each Course
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

    # For Staffs
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
        "meeting_ceo_name_list": meeting_ceo_name_list,
        "topics_ceo_count_list": topics_ceo_count_list,
        "meeting_hr_name_list": meeting_hr_name_list,
        "topics_hr_count_list": topics_hr_count_list,
        "no_hr_meetings": no_hr_meetings,
        "no_ceo_meetings": no_ceo_meetings,
        "meeting_ceo_name": meeting_ceo_name,
        "data_ceo_present": data_ceo_present,
        "data_ceo_absent": data_ceo_absent,
        "meeting_hr_name": meeting_hr_name,
        "data_hr_present": data_hr_present,
        "data_hr_absent": data_hr_absent,
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
    }
    return render(request, "ceo_template/home_content.html", context)


@login_required(login_url='user_login')
def ceo_view_ceo_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceCEOReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'ceo_template/ceo_ceo_attendance.html', context)


@login_required(login_url='user_login')
def ceo_view_hr_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceHRReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'ceo_template/ceo_hr_attendance.html', context)


@login_required(login_url='user_login')
def add_hr(request):
    form = AddHRForm()
    context = {
        "form": form
    }
    return render(request, 'ceo_template/add_hr_template.html', context)


@login_required(login_url='user_login')
def add_hr_save(request):
    if request.method == "POST":
        customer_form = AddCustomerForm(request.POST)
        hr_form = AddHRForm(request.POST)
        if customer_form.is_valid() and hr_form.is_valid():
            first_name = customer_form.cleaned_data['first_name']
            last_name = customer_form.cleaned_data['last_name']
            username = customer_form.cleaned_data['username']
            email = customer_form.cleaned_data['email']
            password = customer_form.cleaned_data['password']
            address = hr_form.cleaned_data['address']
            nida_number = hr_form.cleaned_data['nida_number']

            obj = User.objects.get(id=request.user.id)
            ceo_obj = CEO.objects.get(admin__user=obj)
            office_obj = ceo_obj.office


            user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            customer = S_CustomUser(user=user, user_type = 2)
            customer.save()


            hr = Human_resource_managers(admin=customer, office=office_obj, address=address, nida_number=nida_number)
            hr.save()
            messages.success(request, "HR Added Successfully!")
            return redirect('add_hr')
    else:
        customer_form = AddCustomerForm()
        hr_form = AddHRForm()
        context = {
            'customer_form': customer_form,
            'hr_form': hr_form
        }
        return render(request, 'ceo_template/add_hr_template.html', context)


@login_required(login_url='user_login')
def manage_hr(request):
    obj = User.objects.get(id=request.user.id)
    hr_obj = CEO.objects.get(admin__user=obj)
    office_obj = hr_obj.office
    hrs = Human_resource_managers.objects.filter(office=office_obj)
    context = {
        "hrs": hrs
    }
    return render(request, 'ceo_template/manage_hr_template.html', context)


@login_required(login_url='user_login')
def edit_hr(request, hr_id):
    # Adding Student ID into Session Variable
    request.session['hr_id'] = hr_id

    hr = Human_resource_managers.objects.get(admin=hr_id)
    form = EditHRForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = hr.admin.user.email
    form.fields['username'].initial = hr.admin.user.username
    form.fields['first_name'].initial = hr.admin.user.first_name
    form.fields['last_name'].initial = hr.admin.user.last_name
    form.fields['address'].initial = hr.address


    context = {
        "id": hr_id,
        "username": hr.admin.user.username,
        "form": form
    }
    return render(request, "ceo_template/edit_hr_template.html", context)


@login_required(login_url='user_login')
def edit_hr_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        hr_id = request.session.get('hr_id')
        if hr_id == None:
            return redirect('manage_hr')

        form = EditHRForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']


            try:
                obj = User.objects.get(id=request.user.id)
                ceo_obj = CEO.objects.get(admin__user=obj)
                office_obj = ceo_obj.office
                # First Update into Custom User Model
                user = Human_resource_managers.objects.get(id=hr_id)
                user.admin.user.first_name = first_name
                user.admin.user.last_name = last_name
                user.admin.user.email = email
                user.admin.user.username = username


                # Then Update Students Table

                user.address = address

                user.office = office_obj

                user.save()
                # Delete student_id SESSION after the data is updated
                del request.session['hr_id']

                messages.success(request, "HR Updated Successfully!")
                return redirect('/edit_hr/'+hr_id)
            except:
                messages.success(request, "Failed to Update HR.")
                return redirect('/edit_hr/'+hr_id)
        else:
            return redirect('/edit_hr/'+hr_id)


@login_required(login_url='user_login')
def delete_hr(request, hr_id):
    hr = Human_resource_managers.objects.get(id=hr_id)
    try:
        hr.delete()
        messages.success(request, "HR Deleted Successfully.")
        return redirect('manage_hr')
    except:
        messages.error(request, "Failed to Delete HR.")
        return redirect('manage_hr')


@login_required(login_url='user_login')
def add_goal(request):
    return render(request, "ceo_template/add_goal_template.html")


@login_required(login_url='user_login')
def add_goal_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_goal')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        goal = request.POST.get('goal')
        description = request.POST.get('description')
        try:
            goal_model = Goals(name=goal, office=office, description=description)
            goal_model.save()
            messages.success(request, "Goal Added Successfully!")
            return redirect('add_goal')
        except:
            messages.error(request, "Failed to Add Goal!")
            return redirect('add_goal')


@login_required(login_url='user_login')
def manage_goal(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    goals = Goals.objects.filter(office=office)
    context = {
        "goals": goals
    }
    return render(request, 'ceo_template/manage_goal_template.html', context)


@login_required(login_url='user_login')
def edit_goal(request, goal_id):
    request.session['goal_id'] = goal_id
    goal = Goals.objects.get(id=goal_id)
    context = {
        "goal": goal,
        "id": goal_id
    }
    return render(request, 'ceo_template/edit_goal_template.html', context)


@login_required(login_url='user_login')
def edit_goal_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        goal_id = request.session.get('goal_id')
        name = request.POST.get('goal')
        description = request.POST.get('description')

        try:
            goal = Goals.objects.get(id=goal_id)
            goal.name = name
            goal.description = description
            goal.save()

            messages.success(request, "Goal Updated Successfully.")
            return redirect('/edit_goal/'+goal_id)

        except:
            messages.error(request, "Failed to Update Goal.")
            return redirect('/edit_goal/'+goal_id)


@login_required(login_url='user_login')
def delete_goal(request, goal_id):
    goal = Goals.objects.get(id=goal_id)
    try:
        goal.delete()
        messages.success(request, "Goal Deleted Successfully.")
        return redirect('manage_goal')
    except:
        messages.error(request, "Failed to Delete Goal.")
        return redirect('manage_goal')


@login_required(login_url='user_login')
def add_code_of_conduct(request):
    return render(request, "ceo_template/add_code_of_conduct_template.html")


@login_required(login_url='user_login')
def add_code_of_conduct_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_code_of_conduct')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        code = request.POST.get('code')
        description = request.POST.get('description')
        try:
            code_model = Code_of_Conduct(name=code, office=office, description=description)
            code_model.save()
            messages.success(request, "Conduct Code Added Successfully!")
            return redirect('add_code_of_conduct')
        except:
            messages.error(request, "Failed to Add Conduct Code!")
            return redirect('add_code_of_conduct')


@login_required(login_url='user_login')
def manage_code_of_conduct(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    codes = Code_of_Conduct.objects.filter(office=office)
    context = {
        "codes": codes
    }
    return render(request, 'ceo_template/manage_code_of_conduct_template.html', context)


@login_required(login_url='user_login')
def edit_code_of_conduct(request, code_id):
    request.session['code_id'] = code_id
    code = Code_of_Conduct.objects.get(id=code_id)
    context = {
        "code": code,
        "id": code_id
    }
    return render(request, 'ceo_template/edit_code_of_conduct_template.html', context)


@login_required(login_url='user_login')
def edit_code_of_conduct_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        code_id = request.session.get('code_id')
        name = request.POST.get('code')
        description = request.POST.get('description')

        try:
            code = Code_of_Conduct.objects.get(id=code_id)
            code.name = name
            code.description = description
            code.save()

            messages.success(request, "Conduct Code Updated Successfully.")
            return redirect('/edit_code_of_conduct/'+code_id)

        except:
            messages.error(request, "Failed to Update Conduct Code.")
            return redirect('/edit_resp_hr/'+code_id)


@login_required(login_url='user_login')
def delete_code_of_conduct(request, code_id):
    code = Code_of_Conduct.objects.get(id=code_id)
    try:
        code.delete()
        messages.success(request, "Conduct Code Deleted Successfully.")
        return redirect('manage_code_of_conduct')
    except:
        messages.error(request, "Failed to Delete Conduct Code.")
        return redirect('manage_code_of_conduct')


@login_required(login_url='user_login')
def add_resp_hr(request):
    return render(request, "ceo_template/add_resp_hr_template.html")


@login_required(login_url='user_login')
def add_resp_hr_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_resp_hr')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        name = request.POST.get('name')
        description = request.POST.get('description')
        try:
            resp_hr_model = ResponsibilityHR(name=name, office=office, description=description)
            resp_hr_model.save()
            messages.success(request, "Conduct HR Responsibility Added Successfully!")
            return redirect('add_resp_hr')
        except:
            messages.error(request, "Failed to Add HR Responsibility!")
            return redirect('add_resp_hr')


@login_required(login_url='user_login')
def manage_resp_hr(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    resp_hrs = ResponsibilityHR.objects.filter(office=office)
    context = {
        "resp_hrs": resp_hrs
    }
    return render(request, 'ceo_template/manage_resp_hr_template.html', context)


@login_required(login_url='user_login')
def edit_resp_hr(request, resp_hr_id):
    request.session['resp_hr_id'] = resp_hr_id
    resp_hr = ResponsibilityHR.objects.get(id=resp_hr_id)
    context = {
        "resp_hr": resp_hr,
        "id": resp_hr_id
    }
    return render(request, 'ceo_template/edit_resp_hr_template.html', context)


@login_required(login_url='user_login')
def edit_resp_hr_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        resp_hr_id = request.session.get('resp_hr_id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_hr = ResponsibilityHR.objects.get(id=resp_hr_id)
            resp_hr.name = name
            resp_hr.description = description
            resp_hr.save()

            messages.success(request, "HR Responsibility Updated Successfully.")
            return redirect('/edit_resp_hr/'+resp_hr_id)

        except:
            messages.error(request, "Failed to Update HR Responsibility.")
            return redirect('/edit_resp_hr/'+resp_hr_id)


@login_required(login_url='user_login')
def delete_resp_hr(request, resp_hr_id):
    resp_hr = ResponsibilityHR.objects.get(id=resp_hr_id)
    try:
        resp_hr.delete()
        messages.success(request, "HR Responsibility Deleted Successfully.")
        return redirect('manage_resp_hr')
    except:
        messages.error(request, "Failed to Delete HR Responsibility.")
        return redirect('manage_resp_hr')


@login_required(login_url='user_login')
def add_resp_law(request):
    return render(request, "ceo_template/add_resp_law_template.html")


@login_required(login_url='user_login')
def add_resp_law_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_resp_law')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        name = request.POST.get('name')
        description = request.POST.get('description')
        try:
            resp_law_model = ResponsibilityLawyers(name=name, office=office, description=description)
            resp_law_model.save()
            messages.success(request, "Lawyer Responsibility Added Successfully!")
            return redirect('add_resp_law')
        except:
            messages.error(request, "Failed to Add Lawyer Responsibility!")
            return redirect('add_resp_law')


@login_required(login_url='user_login')
def manage_resp_law(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    resp_laws = ResponsibilityLawyers.objects.all()
    context = {
        "resp_laws": resp_laws
    }
    return render(request, 'ceo_template/manage_resp_law_template.html', context)


@login_required(login_url='user_login')
def edit_resp_law(request, resp_law_id):
    request.session['resp_law_id'] = resp_law_id
    resp_law = ResponsibilityLawyers.objects.get(id=resp_law_id)
    context = {
        "resp_law": resp_law,
        "id": resp_law_id
    }
    return render(request, 'ceo_template/edit_resp_law_template.html', context)


@login_required(login_url='user_login')
def edit_resp_law_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        resp_law_id = request.session.get('resp_law_id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_law = ResponsibilityLawyers.objects.get(id=resp_law_id)
            resp_law.name = name
            resp_law.description = description
            resp_law.save()

            messages.success(request, "Lawyer Responsibility Updated Successfully.")
            return redirect('/edit_resp_law/'+resp_law_id)

        except:
            messages.error(request, "Failed to Update Lawyer Responsibility.")
            return redirect('/edit_resp_law/'+resp_law_id)


@login_required(login_url='user_login')
def delete_resp_law(request, resp_law_id):
    resp_law = ResponsibilityLawyers.objects.get(id=resp_law_id)
    try:
        resp_law.delete()
        messages.success(request, "Lawyer Responsibility Deleted Successfully.")
        return redirect('manage_resp_law')
    except:
        messages.error(request, "Failed to Delete Lawyer Responsibility.")
        return redirect('manage_resp_law')


@login_required(login_url='user_login')
def add_resp_cs(request):
    return render(request, "ceo_template/add_resp_cs_template.html")


@login_required(login_url='user_login')
def add_resp_cs_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_resp_cs')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        name = request.POST.get('name')
        description = request.POST.get('description')
        try:
            resp_cs_model = ResponsibilityCS(name=name, office=office, description=description)
            resp_cs_model.save()
            messages.success(request, "Conduct CS Responsibility Added Successfully!")
            return redirect('add_resp_cs')
        except:
            messages.error(request, "Failed to Add CS Responsibility!")
            return redirect('add_resp_cs')


@login_required(login_url='user_login')
def manage_resp_cs(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    resp_css = ResponsibilityCS.objects.filter(office=office)
    context = {
        "resp_css": resp_css
    }
    return render(request, 'ceo_template/manage_resp_cs_template.html', context)


@login_required(login_url='user_login')
def edit_resp_cs(request, resp_cs_id):
    request.session['resp_cd_id'] = resp_cs_id
    resp_cs = ResponsibilityCS.objects.get(id=resp_cs_id)
    context = {
        "resp_cs": resp_cs,
        "id": resp_cs_id
    }
    return render(request, 'ceo_template/edit_resp_cs_template.html', context)


@login_required(login_url='user_login')
def edit_resp_cs_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        resp_cs_id = request.session.get('resp_cs_id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_cs = ResponsibilityCS.objects.get(id=resp_cs_id)
            resp_cs.name = name
            resp_cs.description = description
            resp_cs.save()

            messages.success(request, "CS Responsibility Updated Successfully.")
            return redirect('/edit_resp_cs/'+resp_cs_id)

        except:
            messages.error(request, "Failed to Update CS Responsibility.")
            return redirect('/edit_resp_cs/'+resp_cs_id)


@login_required(login_url='user_login')
def delete_resp_cs(request, resp_cs_id):
    resp_cs = ResponsibilityCS.objects.get(id=resp_cs_id)
    try:
        resp_cs.delete()
        messages.success(request, "CS Responsibility Deleted Successfully.")
        return redirect('manage_resp_cs')
    except:
        messages.error(request, "Failed to Delete CS Responsibility.")
        return redirect('manage_resp_cs')


@login_required(login_url='user_login')
def add_resp_swo(request):
    return render(request, "ceo_template/add_resp_swo_template.html")


@login_required(login_url='user_login')
def add_resp_swo_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_resp_swo')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        name = request.POST.get('name')
        description = request.POST.get('description')
        try:
            resp_swo_model = ResponsibilitySWO(name=name, office=office, description=description)
            resp_swo_model.save()
            messages.success(request, "Conduct SWO Responsibility Added Successfully!")
            return redirect('add_resp_swo')
        except:
            messages.error(request, "Failed to Add SWO Responsibility!")
            return redirect('add_resp_swo')


@login_required(login_url='user_login')
def manage_resp_swo(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    resp_swos = ResponsibilitySWO.objects.filter(office=office)
    context = {
        "resp_swos": resp_swos
    }
    return render(request, 'ceo_template/manage_resp_swo_template.html', context)


@login_required(login_url='user_login')
def edit_resp_swo(request, resp_swo_id):
    request.session['resp_swo_id'] = resp_swo_id
    resp_swo = ResponsibilitySWO.objects.get(id=resp_swo_id)
    context = {
        "resp_swo": resp_swo,
        "id": resp_swo_id
    }
    return render(request, 'ceo_template/edit_resp_swo_template.html', context)


@login_required(login_url='user_login')
def edit_resp_swo_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        resp_swo_id = request.session.get('resp_swo_id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_swo = ResponsibilitySWO.objects.get(id=resp_swo_id)
            resp_swo.name = name
            resp_swo.description = description
            resp_swo.save()

            messages.success(request, "SWO Responsibility Updated Successfully.")
            return redirect('/edit_resp_swo/'+resp_swo_id)

        except:
            messages.error(request, "Failed to Update SWO Responsibility.")
            return redirect('/edit_resp_swo/'+resp_swo_id)


@login_required(login_url='user_login')
def delete_resp_swo(request, resp_swo_id):
    resp_swo = ResponsibilitySWO.objects.get(id=resp_swo_id)
    try:
        resp_swo.delete()
        messages.success(request, "SWO Responsibility Deleted Successfully.")
        return redirect('manage_resp_swo')
    except:
        messages.error(request, "Failed to Delete SWO Responsibility.")
        return redirect('manage_resp_swo')


@login_required(login_url='user_login')
def add_resp_admin(request):
    return render(request, "ceo_template/add_resp_admin_template.html")


@login_required(login_url='user_login')
def add_resp_admin_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_resp_admin')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        name = request.POST.get('name')
        description = request.POST.get('description')
        try:
            resp_admin_model = ResponsibilityAdmin(name=name, office=office, description=description)
            resp_admin_model.save()
            messages.success(request, "Admin Responsibility Added Successfully!")
            return redirect('add_resp_admin')
        except:
            messages.error(request, "Failed to Add Admin Responsibility!")
            return redirect('add_resp_admin')


@login_required(login_url='user_login')
def manage_resp_admin(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    resp_admins = ResponsibilityAdmin.objects.filter(office=office)
    context = {
        "resp_admins": resp_admins
    }
    return render(request, 'ceo_template/manage_resp_admin_template.html', context)


@login_required(login_url='user_login')
def edit_resp_admin(request, resp_admin_id):
    request.session['resp_admin_id'] = resp_admin_id
    resp_admin = ResponsibilityAdmin.objects.get(id=resp_admin_id)
    context = {
        "resp_admin": resp_admin,
        "id": resp_admin_id
    }
    return render(request, 'ceo_template/edit_resp_admin_template.html', context)


@login_required(login_url='user_login')
def edit_resp_admin_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        resp_admin_id = request.session.get('resp_admin_id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_admin = ResponsibilityAdmin.objects.get(id=resp_admin_id)
            resp_admin.name = name
            resp_admin.description = description
            resp_admin.save()

            messages.success(request, "Admin Responsibility Updated Successfully.")
            return redirect('/edit_resp_admin/'+resp_admin_id)

        except:
            messages.error(request, "Failed to Update Admin Responsibility.")
            return redirect('/edit_resp_admin/'+resp_admin_id)


@login_required(login_url='user_login')
def delete_resp_admin(request, resp_admin_id):
    resp_admin = ResponsibilityAdmin.objects.get(id=resp_admin_id)
    try:
        resp_admin.delete()
        messages.success(request, "Admin Responsibility Deleted Successfully.")
        return redirect('manage_resp_admin')
    except:
        messages.error(request, "Failed to Delete Admin Responsibility.")
        return redirect('manage_resp_admin')


@login_required(login_url='user_login')
def add_resp_acc(request):
    return render(request, "ceo_template/add_resp_acc_template.html")


@login_required(login_url='user_login')
def add_resp_acc_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_resp_acc')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        name = request.POST.get('name')
        description = request.POST.get('description')
        try:
            resp_acc_model = ResponsibilityAccountant(name=name, office=office, description=description)
            resp_acc_model.save()
            messages.success(request, "Conduct Accountant Responsibility Added Successfully!")
            return redirect('add_resp_acc')
        except:
            messages.error(request, "Failed to Add Accountant Responsibility!")
            return redirect('add_resp_acc')


@login_required(login_url='user_login')
def manage_resp_acc(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    resp_accs = ResponsibilityAccountant.objects.filter(office=office)
    context = {
        "resp_accs": resp_accs
    }
    return render(request, 'ceo_template/manage_resp_acc_template.html', context)


@login_required(login_url='user_login')
def edit_resp_acc(request, resp_acc_id):
    request.session['resp_acc_id'] = resp_acc_id
    resp_acc = ResponsibilityAccountant.objects.get(id=resp_acc_id)
    context = {
        "resp_acc": resp_acc,
        "id": resp_acc_id
    }
    return render(request, 'ceo_template/edit_resp_acc_template.html', context)


@login_required(login_url='user_login')
def edit_resp_acc_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        resp_acc_id = request.session.get('resp_acc_id')
        name = request.POST.get('name')
        description = request.POST.get('description')

        try:
            resp_acc = ResponsibilityAccountant.objects.get(id=resp_acc_id)
            resp_acc.name = name
            resp_acc.description = description
            resp_acc.save()

            messages.success(request, "Accountant Responsibility Updated Successfully.")
            return redirect('/edit_resp_acc/'+resp_acc_id)

        except:
            messages.error(request, "Failed to Update Accountant Responsibility.")
            return redirect('/edit_resp_acc/'+resp_acc_id)


@login_required(login_url='user_login')
def delete_resp_acc(request, resp_acc_id):
    resp_acc = ResponsibilityAccountant.objects.get(id=resp_acc_id)
    try:
        resp_acc.delete()
        messages.success(request, "Accountant Responsibility Deleted Successfully.")
        return redirect('manage_resp_acc')
    except:
        messages.error(request, "Failed to Delete Accountant Responsibility.")
        return redirect('manage_resp_acc')


@login_required(login_url='user_login')
def add_salary_hr(request):
    return render(request, "ceo_template/add_salary_hr_template.html")


@login_required(login_url='user_login')
def add_salary_hr_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_hr')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        try:
            salary_hr_model = SalaryHR(amount=amount, office=office, description=description)
            salary_hr_model.save()
            messages.success(request, "HR Salary Added Successfully!")
            return redirect('add_salary_hr')
        except:
            messages.error(request, "Failed to Add HR Salary!")
            return redirect('add_salary_hr')


@login_required(login_url='user_login')
def manage_salary_hr(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    salary_hrs = SalaryHR.objects.filter(office=office)
    context = {
        "salary_hrs": salary_hrs
    }
    return render(request, 'ceo_template/manage_salary_hr_template.html', context)


@login_required(login_url='user_login')
def edit_salary_hr(request, salary_hr_id):
    request.session['salary_hr_id'] = salary_hr_id
    salary_hr = SalaryHR.objects.get(id=salary_hr_id)
    context = {
        "salary_hr": salary_hr,
        "id": salary_hr_id
    }
    return render(request, 'ceo_template/edit_salary_hr_template.html', context)


@login_required(login_url='user_login')
def edit_salary_hr_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        salary_hr_id = request.session.get('salary_hr_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        try:
            salary_hr = SalaryHR.objects.get(id=salary_hr_id)
            salary_hr.amount = amount
            salary_hr.description = description
            salary_hr.save()

            messages.success(request, "HR Salary Updated Successfully.")
            return redirect('/edit_salary_hr/'+salary_hr_id)

        except:
            messages.error(request, "Failed to Update HR Salary.")
            return redirect('/edit_salary_hr/'+salary_hr_id)


@login_required(login_url='user_login')
def delete_salary_hr(request, salary_hr_id):
    salary_hr = SalaryHR.objects.get(id=salary_hr_id)
    try:
        salary_hr.delete()
        messages.success(request, "HR Salary Deleted Successfully.")
        return redirect('manage_salary_hr')
    except:
        messages.error(request, "Failed to Delete HR Salary.")
        return redirect('manage_salary_hr')


@login_required(login_url='user_login')
def add_salary_acc(request):
    return render(request, "ceo_template/add_salary_acc_template.html")


@login_required(login_url='user_login')
def add_salary_acc_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_acc')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        try:
            salary_acc_model = SalaryAccountant(amount=amount, office=office, description=description)
            salary_acc_model.save()
            messages.success(request, "Accountant Salary Added Successfully!")
            return redirect('add_salary_acc')
        except:
            messages.error(request, "Failed to Add Accountant Salary!")
            return redirect('add_salary_acc')


@login_required(login_url='user_login')
def manage_salary_acc(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    salary_accs = SalaryAccountant.objects.filter(office=office)
    context = {
        "salary_accs": salary_accs
    }
    return render(request, 'ceo_template/manage_salary_acc_template.html', context)


@login_required(login_url='user_login')
def edit_salary_acc(request, salary_acc_id):
    request.session['salary_acc_id'] = salary_acc_id
    salary_acc = SalaryAccountant.objects.get(id=salary_acc_id)
    context = {
        "salary_acc": salary_acc,
        "id": salary_acc_id
    }
    return render(request, 'ceo_template/edit_salary_acc_template.html', context)


@login_required(login_url='user_login')
def edit_salary_acc_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        salary_acc_id = request.session.get('salary_acc_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        try:
            salary_acc = SalaryAccountant.objects.get(id=salary_acc_id)
            salary_acc.amount = amount
            salary_acc.description = description
            salary_acc.save()

            messages.success(request, "Accountant Salary Updated Successfully.")
            return redirect('/edit_salary_acc/'+salary_acc_id)

        except:
            messages.error(request, "Failed to Update Accountant Salary.")
            return redirect('/edit_salary_acc/'+salary_acc_id)


@login_required(login_url='user_login')
def delete_salary_acc(request, salary_acc_id):
    salary_acc = SalaryAccountant.objects.get(id=salary_acc_id)
    try:
        salary_acc.delete()
        messages.success(request, "Accountant Salary Deleted Successfully.")
        return redirect('manage_salary_acc')
    except:
        messages.error(request, "Failed to Delete Accountant Salary.")
        return redirect('manage_salary_acc')


@login_required(login_url='user_login')
def add_salary_swo(request):
    return render(request, "ceo_template/add_salary_swo_template.html")


@login_required(login_url='user_login')
def add_salary_swo_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_swo')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        try:
            salary_swo_model = SalarySWO(amount=amount, office=office, description=description)
            salary_swo_model.save()
            messages.success(request, "SWO Salary Added Successfully!")
            return redirect('add_salary_swo')
        except:
            messages.error(request, "Failed to Add SWO Salary!")
            return redirect('add_salary_swo')


@login_required(login_url='user_login')
def manage_salary_swo(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    salary_swos = SalarySWO.objects.filter(office=office)
    context = {
        "salary_swos": salary_swos
    }
    return render(request, 'ceo_template/manage_salary_swo_template.html', context)


@login_required(login_url='user_login')
def edit_salary_swo(request, salary_swo_id):
    request.session['salary_swo_id'] = salary_swo_id
    salary_swo = SalarySWO.objects.get(id=salary_swo_id)
    context = {
        "salary_acc": salary_swo,
        "id": salary_swo_id
    }
    return render(request, 'ceo_template/edit_salary_swo_template.html', context)


@login_required(login_url='user_login')
def edit_salary_swo_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        salary_swo_id = request.session.get('salary_swo_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        try:
            salary_swo = SalarySWO.objects.get(id=salary_swo_id)
            salary_swo.amount = amount
            salary_swo.description = description
            salary_swo.save()

            messages.success(request, "SWO Salary Updated Successfully.")
            return redirect('/edit_salary_swo/'+salary_swo_id)

        except:
            messages.error(request, "Failed to Update SWO Salary.")
            return redirect('/edit_salary_swo/'+salary_swo_id)


@login_required(login_url='user_login')
def delete_salary_swo(request, salary_swo_id):
    salary_swo = SalarySWO.objects.get(id=salary_swo_id)
    try:
        salary_swo.delete()
        messages.success(request, "SWO Salary Deleted Successfully.")
        return redirect('manage_salary_swo')
    except:
        messages.error(request, "Failed to Delete SWO Salary.")
        return redirect('manage_salary_swo')


@login_required(login_url='user_login')
def add_salary_law(request):
    return render(request, "ceo_template/add_salary_law_template.html")


@login_required(login_url='user_login')
def add_salary_law_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_law')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        try:
            salary_law_model = SalaryLawyer(amount=amount, description=description)
            salary_law_model.save()
            messages.success(request, "Lawyer Salary Added Successfully!")
            return redirect('add_salary_law')
        except:
            messages.error(request, "Failed to Add Lawyer Salary!")
            return redirect('add_salary_law')


@login_required(login_url='user_login')
def manage_salary_law(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    salary_laws = SalaryLawyer.objects.filter(office=office)
    context = {
        "salary_laws": salary_laws
    }
    return render(request, 'ceo_template/manage_salary_law_template.html', context)


@login_required(login_url='user_login')
def edit_salary_law(request, salary_law_id):
    request.session['salary_law_id'] = salary_law_id
    salary_law = SalaryLawyer.objects.get(id=salary_law_id)
    context = {
        "salary_law": salary_law,
        "id": salary_law_id
    }
    return render(request, 'ceo_template/edit_salary_law_template.html', context)


@login_required(login_url='user_login')
def edit_salary_law_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        salary_law_id = request.session.get('salary_law_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        try:
            salary_law = SalaryLawyer.objects.get(id=salary_law_id)
            salary_law.amount = amount
            salary_law.description = description
            salary_law.save()

            messages.success(request, "Lawyer Salary Updated Successfully.")
            return redirect('/edit_salary_law/'+salary_law_id)

        except:
            messages.error(request, "Failed to Update Lawyer Salary.")
            return redirect('/edit_salary_law/'+salary_law_id)


@login_required(login_url='user_login')
def delete_salary_law(request, salary_law_id):
    salary_law = SalaryLawyer.objects.get(id=salary_law_id)
    try:
        salary_law.delete()
        messages.success(request, "Lawyer Salary Deleted Successfully.")
        return redirect('manage_salary_law')
    except:
        messages.error(request, "Failed to Delete Lawyer Salary.")
        return redirect('manage_salary_law')


@login_required(login_url='user_login')
def add_salary_admin(request):
    return render(request, "ceo_template/add_salary_admin_template.html")


@login_required(login_url='user_login')
def add_salary_admin_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_admin')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        try:
            salary_admin_model = SalaryAdmin(amount=amount, office=office, description=description)
            salary_admin_model.save()
            messages.success(request, "Admin Salary Added Successfully!")
            return redirect('add_salary_admin')
        except:
            messages.error(request, "Failed to Add Admin Salary!")
            return redirect('add_salary_admin')


@login_required(login_url='user_login')
def manage_salary_admin(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    salary_admins = SalaryAdmin.objects.filter(office=office)
    context = {
        "salary_admins": salary_admins
    }
    return render(request, 'ceo_template/manage_salary_admin_template.html', context)


@login_required(login_url='user_login')
def edit_salary_admin(request, salary_admin_id):
    request.session['salary_admin_id'] = salary_admin_id
    salary_admin = SalaryAdmin.objects.get(id=salary_admin_id)
    context = {
        "salary_admin": salary_admin,
        "id": salary_admin_id
    }
    return render(request, 'ceo_template/edit_salary_admin_template.html', context)


@login_required(login_url='user_login')
def edit_salary_admin_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        salary_admin_id = request.session.get('salary_admin_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        try:
            salary_admin = SalaryAdmin.objects.get(id=salary_admin_id)
            salary_admin.amount = amount
            salary_admin.description = description
            salary_admin.save()

            messages.success(request, "Admin Salary Updated Successfully.")
            return redirect('/edit_salary_admin/'+salary_admin_id)

        except:
            messages.error(request, "Failed to Update Admin Salary.")
            return redirect('/edit_salary_admin/'+salary_admin_id)


@login_required(login_url='user_login')
def delete_salary_admin(request, salary_admin_id):
    salary_admin = SalaryAdmin.objects.get(id=salary_admin_id)
    try:
        salary_admin.delete()
        messages.success(request, "Admin Salary Deleted Successfully.")
        return redirect('manage_salary_admin')
    except:
        messages.error(request, "Failed to Delete Admin Salary.")
        return redirect('manage_salary_admin')


@login_required(login_url='user_login')
def add_salary_cs(request):
    return render(request, "ceo_template/add_salary_cs_template.html")


@login_required(login_url='user_login')
def add_salary_cs_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_salary_cs')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        try:
            salary_cs_model = SalaryCS(amount=amount, office=office, description=description)
            salary_cs_model.save()
            messages.success(request, "CS Salary Added Successfully!")
            return redirect('add_salary_cs')
        except:
            messages.error(request, "Failed to Add CS Salary!")
            return redirect('add_salary_cs')


@login_required(login_url='user_login')
def manage_salary_cs(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    salary_css = SalaryCS.objects.filter(office=office)
    context = {
        "salary_css": salary_css
    }
    return render(request, 'ceo_template/manage_salary_cs_template.html', context)


@login_required(login_url='user_login')
def edit_salary_cs(request, salary_cs_id):
    request.session['salary_cs_id'] = salary_cs_id
    salary_cs = SalaryCS.objects.get(id=salary_cs_id)
    context = {
        "salary_acc": salary_cs,
        "id": salary_cs_id
    }
    return render(request, 'ceo_template/edit_salary_cs_template.html', context)


@login_required(login_url='user_login')
def edit_salary_cs_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        salary_cs_id = request.session.get('salary_cs_id')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        try:
            salary_cs = SalaryCS.objects.get(id=salary_cs_id)
            salary_cs.amount = amount
            salary_cs.description = description
            salary_cs.save()

            messages.success(request, "CS Salary Updated Successfully.")
            return redirect('/edit_salary_cs/'+salary_cs_id)

        except:
            messages.error(request, "Failed to Update CS Salary.")
            return redirect('/edit_salary_cs/'+salary_cs_id)


@login_required(login_url='user_login')
def delete_salary_cs(request, salary_cs_id):
    salary_cs = SalaryCS.objects.get(id=salary_cs_id)
    try:
        salary_cs.delete()
        messages.success(request, "CS Salary Deleted Successfully.")
        return redirect('manage_salary_cs')
    except:
        messages.error(request, "Failed to Delete CS Salary.")
        return redirect('manage_salary_cs')


@login_required(login_url='user_login')
def ceo_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    leave_data = LeaveReportCEO.objects.filter(ceo_id=ceo_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'ceo_template/ceo_apply_leave.html', context)


@login_required(login_url='user_login')
def ceo_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('ceo_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportCEO(ceo_id=ceo_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('ceo_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('ceo_apply_leave')


@login_required(login_url='user_login')
def ceo_apply_permission(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    permission_data = PermissionReportCEO.objects.filter(ceo_id=ceo_obj)
    context = {
        "permission_data": permission_data
    }
    return render(request, 'ceo_template/ceo_apply_permission.html', context)


@login_required(login_url='user_login')
def ceo_apply_permission_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('ceo_permission_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        try:
            leave_report = PermissionReportCEO(ceo_id=ceo_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('ceo_apply_permission')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('ceo_apply_permission')


@login_required(login_url='user_login')
def ceo_feedback(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    feedback_data = FeedBackCEO.objects.filter(ceo_id=ceo_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'ceo_template/ceo_feedback.html', context)


@login_required(login_url='user_login')
def ceo_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('ceo_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)


        try:
            add_feedback = FeedBackCEO(ceo_id=ceo_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('ceo_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('ceo_feedback')


@login_required(login_url='user_login')
def hr_feedback_message(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    feedbacks = FeedBackHR.objects.filter(hr_id__office=office)
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'ceo_template/hr_feedback_template.html', context)


@csrf_exempt
def hr_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackHR.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


@login_required(login_url='user_login')
def add_notification_hr(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    hrs = Human_resource_managers.objects.filter(office=office)
    context = {
        "hrs": hrs
    }
    return render(request, 'ceo_template/add_hr_notification_template.html', context)


@login_required(login_url='user_login')
def add_notification_hr_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_notification_hr')
    else:
        message = request.POST.get('message')

        hr_id = request.POST.get('hr')
        hr = Human_resource_managers.objects.get(id=hr_id)

        try:
            hr_notification = NotificationHR(message=message, hr_id=hr)
            hr_notification.save()
            messages.success(request, "Notification Sent Successfully!")
            return redirect('add_notification_hr')
        except:
            messages.error(request, "Failed to Send Notification!")
            return redirect('add_notification_hr')


@login_required(login_url='user_login')
def manage_notification_hr(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    notification_hrs = NotificationHR.objects.filter(hr_id__office=office)
    context = {
        "notification_hrs": notification_hrs
    }
    return render(request, 'ceo_template/manage_hr_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_hr(request, hr_id):
    request.session['hr_id'] = hr_id

    hr = Human_resource_managers.objects.get(id=hr_id)
    context = {
        "hr": hr,
        "id": hr_id
    }
    return render(request, 'ceo_template/edit_hr_notification_template.html', context)


@login_required(login_url='user_login')
def edit_notification_hr_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        hr_id = request.session.get('hr_id')
        message = request.POST.get('message')
        hr = Human_resource_managers.objects.get(id=hr_id)

        try:
            hr_notification = NotificationHR(message=message, hr_id=hr)
            hr_notification.save()

            del request.session['hr_id']
            messages.success(request, "Notification Sent Successfully!")
            return redirect('/edit_notification_hr/' + hr_id)

        except:
            messages.error(request, "Failed to Send Notification.")
            return redirect('/edit_notification_hr/' + hr_id)
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_notification_hr(request, notification_hr_id):
    notification_hr = NotificationHR.objects.get(id=notification_hr_id)
    try:
        notification_hr.delete()
        messages.success(request, "Notification Deleted Successfully.")
        return redirect('manage_notification_hr')
    except:
        messages.error(request, "Failed to Delete Notification.")
        return redirect('manage_notification_hr')


@login_required(login_url='user_login')
def add_ceo_meeting(request):
    return render(request, "ceo_template/add_ceo_meeting_template.html")


@login_required(login_url='user_login')
def add_ceo_meeting_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_ceo_meeting')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        office = ceo_obj.office
        name = request.POST.get('name')
        date = request.POST.get('date')
        try:
            meeting_model = CEOMeeting(meeting_name=name, office=office, date=date)
            meeting_model.save()
            messages.success(request, "Meeting Added Successfully!")
            return redirect('add_ceo_meeting')
        except:
            messages.error(request, "Failed to Add Meeting!")
            return redirect('add_ceo_meeting')


@login_required(login_url='user_login')
def manage_ceo_meeting(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    meetings = CEOMeeting.objects.filter(office=office)
    context = {
        "meetings": meetings
    }
    return render(request, 'ceo_template/manage_ceo_meeting_template.html', context)


@login_required(login_url='user_login')
def edit_ceo_meeting(request, meeting_id):
    request.session['meeting_id'] = meeting_id
    meeting = CEOMeeting.objects.get(id=meeting_id)
    context = {
        "meeting": meeting,
        "id": meeting_id
    }
    return render(request, 'ceo_template/edit_ceo_meeting_template.html', context)


@login_required(login_url='user_login')
def edit_ceo_meeting_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        ceo_meeting_id = request.session.get('ceo_meeting_id')
        name = request.POST.get('name')
        date = request.POST.get('date')

        try:
            meeting = CEOMeeting.objects.get(id=ceo_meeting_id)
            meeting.meeting_name = name
            meeting.date = date
            meeting.save()

            messages.success(request, "Meeting Updated Successfully.")
            return redirect('/edit_ceo_meeting/'+ceo_meeting_id)

        except:
            messages.error(request, "Failed to Update Meeting.")
            return redirect('/edit_ceo_meeting/'+ceo_meeting_id)


@login_required(login_url='user_login')
def delete_ceo_meeting(request, meeting_id):
    meeting = CEOMeeting.objects.get(id=meeting_id)
    topics = CEOTopics.objects.filter(meeting_id=meeting)
    attendances = AttendanceCEOReport.objects.filter(meeting_id=meeting)
    try:
        for topic in topics:
            topic.delete()
        for attendance in attendances:
            attendance.delete()
        meeting.delete()
        messages.success(request, "Meeting Deleted Successfully.")
        return redirect('manage_ceo_meeting')
    except:
        messages.error(request, "Failed to Delete Meeting.")
        return redirect('manage_ceo_meeting')


@login_required(login_url='user_login')
def add_ceo_topics(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    meetings = CEOMeeting.objects.filter(office=office)
    context = {
        "meetings": meetings,
    }
    return render(request, 'ceo_template/add_topic_template.html', context)


@login_required(login_url='user_login')
def add_ceo_topics_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_ceo_topics')
    else:
        user = User.objects.get(id=request.user.id)
        ceo_obj = CEO.objects.get(admin__user=user)
        topic_name = request.POST.get('topic')

        meeting_id = request.POST.get('meeting')
        meeting = CEOMeeting.objects.get(id=meeting_id)

        try:
            topic = CEOTopics(topic_name=topic_name, meeting_id=meeting, ceo_id=ceo_obj)
            topic.save()
            messages.success(request, "Agenda Added Successfully!")
            return redirect('add_ceo_topics')
        except:
            messages.error(request, "Failed to Add Agenda!")
            return redirect('add_ceo_topics')


@login_required(login_url='user_login')
def manage_ceo_topics(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    topics = CEOTopics.objects.filter(ceo_id=ceo_obj).order_by('meeting_id')
    context = {
        "topics": topics
    }
    return render(request, 'ceo_template/manage_topic_template.html', context)


@login_required(login_url='user_login')
def edit_ceo_topics(request, topic_id):
    request.session['topic_id'] = topic_id
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    office = ceo_obj.office
    topic = CEOTopics.objects.get(id=topic_id)
    meetings = CEOMeeting.objects.filter(office=office)
    context = {
        "topic": topic,
        "meetings": meetings,
        "id": topic_id
    }
    return render(request, 'ceo_template/edit_topic_template.html', context)


@login_required(login_url='user_login')
def edit_ceo_topics_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        topic_id = request.session.get('topic_id')
        topic_name = request.POST.get('topic')
        meeting_id = request.POST.get('meeting')

        try:
            topic = CEOTopics.objects.get(id=topic_id)
            topic.topic_name = topic_name

            meeting = CEOMeeting.objects.get(id=meeting_id)
            topic.meeting_id = meeting
            topic.save()

            messages.success(request, "Agenda Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_ceo_topic", kwargs={"topic_id": topic_id}))

        except:
            messages.error(request, "Failed to Update Agenda.")
            return HttpResponseRedirect(reverse("edit_ceo_topic", kwargs={"topic_id": topic_id}))
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_ceo_topics(request, topic_id):
    topic = CEOTopics.objects.get(id=topic_id)
    try:
        topic.delete()
        messages.success(request, "Topic Deleted Successfully.")
        return redirect('manage_ceo_topic')
    except:
        messages.error(request, "Failed to Delete Topic.")
        return redirect('manage_ceo_topic')


@login_required(login_url='user_login')
def ceo_view_notification(request):
    user = User.objects.get(id=request.user.id)
    ceo = CEO.objects.get(admin__user=user)
    notifications = NotificationCEO.objects.filter(ceo_id=ceo.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "ceo_template/ceo_view_notification.html", context)


@login_required(login_url='user_login')
def ceo_view_def_notification(request):
    user = User.objects.get(id=request.user.id)
    ceo = CEO.objects.get(admin__user=user)
    def_notifications = DefendantNotificationCEO.objects.filter(ceo_id=ceo.id)
    context = {
        "notifications": def_notifications,
    }
    return render(request, "ceo_template/ceo_view_def_notification.html", context)


@login_required(login_url='user_login')
def ceo_view_acu_notification(request):
    user = User.objects.get(id=request.user.id)
    ceo = CEO.objects.get(admin__user=user)
    acu_notifications = AccusserNotificationCEO.objects.filter(ceo_id=ceo.id)
    context = {
        "notifications": acu_notifications,
    }
    return render(request, "ceo_template/ceo_view_acu_notification.html", context)


@login_required(login_url='user_login')
def hr_leave_view(request):
    user = User.objects.get(id=request.user.id)
    ceo = CEO.objects.get(admin__user=user)
    office = ceo.office
    leaves = LeaveReportHR.objects.filter(hr_id__office=office)
    context = {
        "leaves": leaves
    }
    return render(request, 'ceo_template/hr_leave_view.html', context)


@login_required(login_url='user_login')
def hr_leave_approve(request, leave_id):
    leave = LeaveReportHR.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('hr_leave_view')


@login_required(login_url='user_login')
def hr_leave_reject(request, leave_id):
    leave = LeaveReportHR.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('hr_leave_view')


@login_required(login_url='user_login')
def hr_permission_view(request):
    user = User.objects.get(id=request.user.id)
    ceo = CEO.objects.get(admin__user=user)
    office = ceo.office
    permissions = PermissionReportHR.objects.filter(hr_id__office=office)
    context = {
        "permissions": permissions
    }
    return render(request, 'ceo_template/hr_permission_view.html', context)


@login_required(login_url='user_login')
def hr_permission_approve(request, permission_id):
    permission = PermissionReportHR.objects.get(id=permission_id)
    permission.leave_status = 1
    permission.save()
    return redirect('hr_permission_view')


@login_required(login_url='user_login')
def hr_permission_reject(request, permission_id):
    permission = PermissionReportHR.objects.get(id=permission_id)
    permission.leave_status = 2
    permission.save()
    return redirect('hr_permission_view')


@login_required(login_url='user_login')
def ceo_take_attendance(request, meeting_id):
    request.session['meeting_id'] = meeting_id

    meeting = CEOMeeting.objects.get(id=meeting_id)
    attendances = AttendanceCEOReport.objects.filter(meeting_id=meeting)

    user = User.objects.get(id=request.user.id)
    ceo = CEO.objects.get(admin__user=user)
    office = ceo.office
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
    return render(request, "ceo_template/take_attendance_template.html", context)


@login_required(login_url='user_login')
def ceo_meeting_attendance_approve(request, attendance_id):
    att = AttendanceCEOReport.objects.get(id=attendance_id)
    att.status = 1
    att.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def ceo_meeting_attendance_reject(request, attendance_id):
    att = AttendanceCEOReport.objects.get(id=attendance_id)
    att.status = 2
    att.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def ceo_attend_ceo_save(request, ceo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = CEO.objects.get(id=ceo_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def ceo_not_attend_ceo_save(request, ceo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = CEO.objects.get(id=ceo_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def hr_attend_ceo_save(request, hr_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Human_resource_managers.objects.get(id=hr_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def hr_not_attend_ceo_save(request, hr_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Human_resource_managers.objects.get(id=hr_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def swo_attend_ceo_save(request, swo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Social_welfare_officers.objects.get(id=swo_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def swo_not_attend_ceo_save(request, swo_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Social_welfare_officers.objects.get(id=swo_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def law_attend_ceo_save(request, law_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Lawyers.objects.get(id=law_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def law_not_attend_ceo_save(request, law_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Lawyers.objects.get(id=law_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def cs_attend_ceo_save(request, cs_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Customer_service.objects.get(id=cs_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def cs_not_attend_ceo_save(request, cs_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Customer_service.objects.get(id=cs_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def acc_attend_ceo_save(request, acc_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Accountant.objects.get(id=acc_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def acc_not_attend_ceo_save(request, acc_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = Accountant.objects.get(id=acc_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def h_admin_attend_ceo_save(request, h_admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = H_AdminHOD.objects.get(id=h_admin_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def h_admin_not_attend_ceo_save(request, h_admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = H_AdminHOD.objects.get(id=h_admin_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def admin_attend_ceo_save(request, admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = AdminHOD.objects.get(id=admin_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=1)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def admin_not_attend_ceo_save(request, admin_id):
    meeting_id = request.session.get('meeting_id')
    meeting = CEOMeeting.objects.get(id=meeting_id)
    att = AdminHOD.objects.get(id=admin_id)
    attendant_id = att.admin

    attendance = AttendanceCEOReport(meeting_id=meeting, attendant_id=attendant_id, status=2)
    attendance.save()
    return redirect('ceo_take_attendance')


@login_required(login_url='user_login')
def ceo_profile(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = CEO.objects.get(admin__user=user)
    context={
        "user": user,
        "ceo": ceo_obj,
    }
    return render(request, 'ceo_template/ceo_profile.html', context)


@login_required(login_url='user_login')
def ceo_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('ceo_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.get(id=request.user.id)
            ceo_obj = CEO.objects.get(admin__user=user)
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
            return redirect('ceo_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('ceo_profile')


@login_required(login_url='user_login')
def my_view_ceo_resp(request):
    obj = User.objects.get(id=request.user.id)
    user_obj = CEO.objects.get(admin__user=obj)
    office = user_obj.office
    resps = ResponsibilityCEO.objects.all()
    context = {
        "resps": resps
    }
    return render(request, 'ceo_template/view_ceo_resp.html', context)
