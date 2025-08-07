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

from apartment.models import Album

from .models import *
from .forms import *


@login_required(login_url='user_login')
def acc_home(request):
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
    acc_obj = S_CustomUser.objects.get(user=user)
    met_obj = Accountant.objects.get(admin=acc_obj)
    office = met_obj.office
    total_hr_attendance = AttendanceHRReport.objects.filter(attendant_id=acc_obj).count()
    attendance_hr_present = AttendanceHRReport.objects.filter(attendant_id=acc_obj, status=1).count()
    attendance_hr_absent = AttendanceHRReport.objects.filter(attendant_id=acc_obj, status=2).count()
    total_ceo_attendance = AttendanceCEOReport.objects.filter(attendant_id=acc_obj).count()
    attendance_ceo_present = AttendanceCEOReport.objects.filter(attendant_id=acc_obj, status=1).count()
    attendance_ceo_absent = AttendanceCEOReport.objects.filter(attendant_id=acc_obj, status=2).count()
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

    if SalaryHR.objects.filter(office=office).exists() and Human_resource_managers.objects.filter(office=office).exists():
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

    if SalarySWO.objects.filter(office=office).exists() and Social_welfare_officers.objects.filter(office=office).exists():
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

    meeting_ceo_name = []
    data_ceo_present = []
    data_ceo_absent = []
    meeting_ceo_data = CEOMeeting.objects.filter(office=met_obj.office)
    for subject in meeting_ceo_data:
        attendance_present_count = AttendanceCEOReport.objects.filter(meeting_id=subject.id, status=1,
                                                                      attendant_id=acc_obj.id).count()
        attendance_absent_count = AttendanceCEOReport.objects.filter(meeting=subject.id, status=2,
                                                                     attendant_id=acc_obj.id).count()
        meeting_ceo_name.append(subject.meeting_name)
        data_ceo_present.append(attendance_present_count)
        data_ceo_absent.append(attendance_absent_count)

    meeting_hr_name = []
    data_hr_present = []
    data_hr_absent = []

    meeting_hr_data = HRMeeting.objects.filter(office=met_obj.office)
    for subject in meeting_hr_data:
        attendance_present_count = AttendanceHRReport.objects.filter(meeting=subject.id, status=1,
                                                                     attendant_id=acc_obj.id).count()
        attendance_absent_count = AttendanceHRReport.objects.filter(meeting_id=subject.id, status=1,
                                                                    attendant_id=acc_obj.id).count()
        meeting_hr_name.append(subject.meeting_name)
        data_hr_present.append(attendance_present_count)
        data_hr_absent.append(attendance_absent_count)

    context = {
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
        "all_cs_count": all_cs_count,
        "all_ceo_count": all_ceo_count,
        "all_h_admin_count": all_h_admin_count,
        "all_admin_count": all_admin_count,
        "all_accountant_count": all_accountant_count,
        "all_office_count": all_office_count,
        "all_lawyer_count": all_lawyer_count,
        "all_swo_count": all_swo_count,
        "all_hr_count": all_hr_count,
        "total_staff": total_staff
    }
    return render(request, "acc_template/acc_home_template.html", context)


@login_required(login_url='user_login')
def acc_view_ceo_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceCEOReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'acc_template/acc_ceo_attendance.html', context)


@login_required(login_url='user_login')
def acc_view_hr_attendance(request):
    user = User.objects.get(id=request.user.id)
    obj = S_CustomUser.objects.get(user=user)
    attendances = AttendanceHRReport.objects.filter(attendant_id=obj)
    context = {
        "attendances": attendances
    }
    return render(request, 'acc_template/acc_hr_attendance.html', context)


@login_required(login_url='user_login')
def acc_feedback(request):
    user = User.objects.get(id=request.user.id)
    acc_obj = Accountant.objects.get(admin__user=user)
    feedback_data = FeedBackAccountant.objects.filter(accountant_id=acc_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'acc_template/acc_feedback.html', context)


@login_required(login_url='user_login')
def acc_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('acc_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        user = User.objects.get(id=request.user.id)
        acc_obj = Accountant.objects.get(admin__user=user)

        try:
            add_feedback = FeedBackAccountant(accountant_id=acc_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('acc_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('acc_feedback')


@login_required(login_url='user_login')
def acc_apply_leave(request):
    user = User.objects.get(id=request.user.id)
    acc_obj = Accountant.objects.get(admin__user=user)
    leave_data = LeaveReportAccountant.objects.filter(accountant_id=acc_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'acc_template/acc_apply_leave.html', context)


@login_required(login_url='user_login')
def acc_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('acc_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        acc_obj = Accountant.objects.get(admin__user=user)
        try:
            leave_report = LeaveReportAccountant(accountant_id=acc_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('acc_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('acc_apply_leave')


@login_required(login_url='user_login')
def acc_apply_permission(request):
    user = User.objects.get(id=request.user.id)
    acc_obj = Accountant.objects.get(admin__user=user)
    permission_data = PermissionReportAccountant.objects.filter(accountant_id=acc_obj)
    context = {
        "permission_data": permission_data
    }
    return render(request, 'acc_template/acc_apply_permission.html', context)


@login_required(login_url='user_login')
def acc_apply_permission_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('acc_permission_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        user = User.objects.get(id=request.user.id)
        acc_obj = Accountant.objects.get(admin__user=user)
        try:
            leave_report = PermissionReportAccountant(accountant_id=acc_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('acc_apply_permission')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('acc_apply_permission')


@login_required(login_url='user_login')
def acc_view_notification(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    notifications = NotificationAccountant.objects.filter(accountant_id=acc.id)
    context = {
        "notifications": notifications,
    }
    return render(request, "acc_template/acc_view_notification.html", context)


@login_required(login_url='user_login')
def acc_view_def_notification(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    def_notifications = DefendantNotificationAccountant.objects.filter(accountant_id=acc.id)
    context = {
        "notifications": def_notifications,
    }
    return render(request, "acc_template/acc_view_def_notification.html", context)


@login_required(login_url='user_login')
def acc_view_acu_notification(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    acu_notifications = AccusserNotificationAccountant.objects.filter(accountant_id=acc.id)
    context = {
        "notifications": acu_notifications,
    }
    return render(request, "acc_template/acc_view_acu_notification.html", context)


@login_required(login_url='user_login')
def add_a_payment(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office
    town = office.town
    apartments = Album.objects.filter(town=town)
    context = {
        "apartments": apartments
    }
    return render(request, 'acc_template/add_a_payment_template.html', context)


@login_required(login_url='user_login')
def add_a_payment_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_a_payment')
    else:
        user = User.objects.get(id=request.user.id)
        acc = Accountant.objects.get(admin__user=user)
        office = acc.office
        amount = request.POST.get('amount')
        receipt_number = request.POST.get('receipt_number')
        payment_method = request.POST.get('payment_method')

        apartment_id = request.POST.get('apartment')
        payed_object = Album.objects.get(id=apartment_id)

        try:
            a_payment = ApartmentPayment(office=office, amount=amount, receipt_number=receipt_number,
                                     payment_method=payment_method, payed_object=payed_object)
            a_payment.save()
            messages.success(request, "Payment Added Successfully!")
            return redirect('add_a_payment')
        except:
            messages.error(request, "Failed to Add Payment!")
            return redirect('add_a_payment')


@login_required(login_url='user_login')
def manage_a_payment(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office
    a_payments = HotelPayment.objects.filter(office=office)
    context = {
        "a_payments": a_payments
    }
    return render(request, 'acc_template/manage_a_payment_template.html', context)


@login_required(login_url='user_login')
def edit_a_payment(request, a_payment_id):
    request.session['a_payment_id'] = a_payment_id
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office
    town = office.town
    apartments = Album.objects.filter(town=town)
    a_payment = ApartmentPayment.objects.get(id=a_payment_id)
    context = {
        "a_payment": a_payment,
        "apartments": apartments,
        "id": a_payment_id
    }
    return render(request, 'acc_template/edit_a_payment_template.html', context)


@login_required(login_url='user_login')
def edit_a_payment_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        a_payment_id = request.session.get('a_payment_id')
        amount = request.POST.get('amount')
        receipt_number = request.POST.get('receipt_number')
        payment_method = request.POST.get('payment_method')

        apartment_id = request.POST.get('apartment')

        try:
            a_payment = ApartmentPayment.objects.get(id=a_payment_id)
            a_payment.amount = amount

            payed_object = Album.objects.get(id=apartment_id)
            a_payment.payed_object = payed_object

            a_payment.receipt_number = receipt_number
            a_payment.payment_method = payment_method

            a_payment.save()

            messages.success(request, "Payment Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_a_payment", kwargs={"a_payment_id": a_payment_id}))

        except:
            messages.error(request, "Failed to Update Payment.")
            return HttpResponseRedirect(reverse("edit_a_payment", kwargs={"a_payment_id": a_payment_id}))
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_a_payment(request, a_payment_id):
    a_payment = ApartmentPayment.objects.get(id=a_payment_id)
    try:
        a_payment.delete()
        messages.success(request, "Payment Deleted Successfully.")
        return redirect('manage_a_payment')
    except:
        messages.error(request, "Failed to Delete Payment.")
        return redirect('manage_a_payment')


@login_required(login_url='user_login')
def add_income(request):
    return render(request, 'acc_template/add_income_template.html')


@login_required(login_url='user_login')
def add_income_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_income')
    else:
        user = User.objects.get(id=request.user.id)
        acc = Accountant.objects.get(admin__user=user)
        office = acc.office
        amount = request.POST.get('amount')
        receipt_number = request.POST.get('receipt_number')
        payment_method = request.POST.get('payment_method')
        reason = request.POST.get('reason')


        try:
            income = Incomes(office=office, amount=amount, receipt_number=receipt_number,
                                     payment_method=payment_method, reason=reason)
            income.save()
            messages.success(request, "Income Added Successfully!")
            return redirect('add_income')
        except:
            messages.error(request, "Failed to Add Income!")
            return redirect('add_income')


@login_required(login_url='user_login')
def manage_income(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office
    incomes = Incomes.objects.filter(office=office)
    context = {
        "incomes": incomes
    }
    return render(request, 'acc_template/manage_income_template.html', context)


@login_required(login_url='user_login')
def edit_income(request, income_id):
    request.session['income_id'] = income_id
    income = Incomes.objects.get(id=income_id)
    context = {
        "income": income,
        "id": income_id
    }
    return render(request, 'acc_template/edit_income_template.html', context)


@login_required(login_url='user_login')
def edit_income_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        income_id = request.session.get('income_id')
        amount = request.POST.get('amount')
        receipt_number = request.POST.get('receipt_number')
        payment_method = request.POST.get('payment_method')
        reason = request.POST.get('reason')

        try:
            income = Incomes.objects.get(id=income_id)
            income.amount = amount
            income.receipt_number = receipt_number
            income.payment_method = payment_method
            income.reason = reason

            income.save()

            messages.success(request, "Income Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_income", kwargs={"income_id": income_id}))

        except:
            messages.error(request, "Failed to Update Income.")
            return HttpResponseRedirect(reverse("edit_income", kwargs={"income_id": income_id}))
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_income(request, income_id):
    income = Incomes.objects.get(id=income_id)
    try:
        income.delete()
        messages.success(request, "Income Deleted Successfully.")
        return redirect('manage_income')
    except:
        messages.error(request, "Failed to Delete Income.")
        return redirect('manage_income')


@login_required(login_url='user_login')
def add_overdue(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office
    ceos = CEO.objects.filter(office=office)
    swos = Social_welfare_officers.objects.filter(office=office)
    accs = Accountant.objects.filter(office=office)
    hrs = Human_resource_managers.objects.filter(office=office)
    lawyers = Lawyers.objects.all()
    css = Customer_service.objects.filter(office=office)
    admins = AdminHOD.objects.filter(office=office)
    h_admins = H_AdminHOD.objects.filter(office=office)
    context = {
        "ceos": ceos,
        "swos": swos,
        "accs": accs,
        "hrs": hrs,
        "lawyers": lawyers,
        "css": css,
        "admins": admins,
        "h_admins": h_admins,
    }
    return render(request, 'acc_template/add_overdue_template.html', context)


@login_required(login_url='user_login')
def add_overdue_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_overdue')
    else:
        user = User.objects.get(id=request.user.id)
        acc = Accountant.objects.get(admin__user=user)
        office = acc.office
        amount = request.POST.get('amount')
        year = request.POST.get('year')
        description = request.POST.get('description')
        custom_id = request.POST.get('name')

        name = S_CustomUser.objects.get(id=custom_id.admin)

        try:
            overdue = Overdue(name=name, amount=amount, office=office, year=year, description=description)
            overdue.save()
            messages.success(request, "Overdue Added Successfully!")
            return redirect('add_overdue')
        except:
            messages.error(request, "Failed to Add Overdue!")
            return redirect('add_overdue')


@login_required(login_url='user_login')
def manage_overdue(request):
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office
    overdues = Overdue.objects.filter(office=office).order_by('year')
    context = {
        "overdues": overdues
    }
    return render(request, 'acc_template/manage_overdue_template.html', context)


@login_required(login_url='user_login')
def edit_overdue(request, overdue_id):
    request.session['overdue_id'] = overdue_id
    overdue = Overdue.objects.get(id=overdue_id)
    context = {
        "overdue": overdue,
        "id": overdue_id
    }
    return render(request, 'acc_template/edit_overdue_template.html', context)


@login_required(login_url='user_login')
def edit_overdue_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        overdue_id = request.session.get('overdue_id')
        amount = request.POST.get('amount')
        year = request.POST.get('year')
        description = request.POST.get('description')

        try:
            overdue = Overdue.objects.get(id=overdue_id)
            overdue.amount = amount
            overdue.year = year
            overdue.description = description

            overdue.save()

            messages.success(request, "Overdue Updated Successfully.")
            # return redirect('/edit_subject/'+subject_id)
            return HttpResponseRedirect(reverse("edit_overdue", kwargs={"overdue_id": overdue_id}))

        except:
            messages.error(request, "Failed to Update Overdue.")
            return HttpResponseRedirect(reverse("edit_overdue", kwargs={"overdue_id": overdue_id}))
            # return redirect('/edit_subject/'+subject_id)


@login_required(login_url='user_login')
def delete_overdue(request, overdue_id):
    overdue = Overdue.objects.get(id=overdue_id)
    try:
        overdue.delete()
        messages.success(request, "Expenses Deleted Successfully.")
        return redirect('manage_overdue')
    except:
        messages.error(request, "Failed to Delete Overdue.")
        return redirect('manage_overdue')


@csrf_exempt
def get_staffs(request):
    # Getting Values from Ajax POST 'Fetch Student'
    user = User.objects.get(id=request.user.id)
    acc = Accountant.objects.get(admin__user=user)
    office = acc.office

    category = request.POST.get("category")

    if category == 'CEO':
        names = CEO.objects.filter(office=office)
    elif category == 'SWO':
        names = Social_welfare_officers.objects.filter(office=office)
    elif category == 'Accountant':
        names = Accountant.objects.filter(office=office)
    elif category == 'HR':
        names = Human_resource_managers.objects.filter(office=office)
    elif category == 'Lawyer':
        names = Lawyers.objects.all()
    elif category == 'Customer Service':
        names = Customer_service.objects.filter(office=office)
    elif category == 'Apartment Admin':
        names = AdminHOD.objects.filter(office=office)
    elif category == 'Hotel Admin':
        names = H_AdminHOD.objects.filter(office=office)
    else:
        names = ""


    # Only Passing Student Id and Student Name Only
    list_data = []


    for name in names:
        data_small={"id":name.id, "name":name.admin.user.first_name+" "+name.admin.user.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@login_required(login_url='user_login')
def acc_profile(request):
    user = User.objects.get(id=request.user.id)
    ceo_obj = Accountant.objects.get(admin__user=user)
    context={
        "user": user,
        "ceo": ceo_obj,
    }
    return render(request, 'acc_template/acc_profile.html', context)


@login_required(login_url='user_login')
def acc_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('acc_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = User.objects.get(id=request.user.id)
            ceo_obj = Accountant.objects.get(admin__user=user)
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
            return redirect('acc_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('acc_profile')


@login_required(login_url='user_login')
def my_view_acc_resp(request):
    obj = User.objects.get(id=request.user.id)
    user_obj = Accountant.objects.get(admin__user=obj)
    office = user_obj.office
    resps = ResponsibilityAccountant.objects.filter(office=office)
    context = {
        "resps": resps
    }
    return render(request, 'acc_template/view_acc_resp.html', context)
