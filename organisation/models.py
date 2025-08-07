from django.contrib.auth.models import AbstractUser, AbstractBaseUser, User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
import uuid
from django.shortcuts import reverse
from django.db import models
from apartment.models import Drivers, Apartment_owners, Tenants, Album
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class S_CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "or_user")
    last_login = models.DateTimeField(auto_now=True)
    user_type_data = (
    (1, "CEO"), (2, "Human_resource_managers"), (3, "Social_welfare_officers"), (4, "Lawyers"), (5, "Customer_service"), (6, "Accountant"), (7, "H_AdminHOD"), (8, "AdminHOD"), (9, "DC"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Rate(models.Model):
    id = models.AutoField(primary_key=True)
    rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Office(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=70)
    spec_location = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    town = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CEO(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name= "or_ceo")
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    address = models.TextField()
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Human_resource_managers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name= "or_hr")
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    address = models.TextField()
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Lawyers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name= "or_l")
    address = models.TextField()
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer_service(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name= "or_cs")
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Accountant(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name= "or_a")
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Social_welfare_officers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name= "or_swo")
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    address = models.TextField()
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class H_AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name= "h_a_customer")
    address = models.TextField()
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    address = models.TextField()
    nida_number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Discpline_committee(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    h_name = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="head_name")
    s_name = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name="secretary_name")
    ceo = models.ForeignKey(CEO, on_delete=models.CASCADE)
    hr = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    apartment_driver = models.ForeignKey(Drivers, on_delete=models.CASCADE)
    hotel_admin = models.ForeignKey(H_AdminHOD, on_delete=models.CASCADE)
    apartment_admin = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyers, on_delete=models.CASCADE)
    accountant = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    cs = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    swo = models.ForeignKey(Social_welfare_officers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccuserNotificationHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackLawyer(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer_id = models.ForeignKey(Lawyers, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationLawyer(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer_id = models.ForeignKey(Lawyers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationLawyer(models.Model):
    id = models.AutoField(primary_key=True)
    laywer_id = models.ForeignKey(Lawyers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationLawyer(models.Model):
    id = models.AutoField(primary_key=True)
    laywer_id = models.ForeignKey(Lawyers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackSWO(models.Model):
    id = models.AutoField(primary_key=True)
    swo_id = models.ForeignKey(Social_welfare_officers, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationSWO(models.Model):
    id = models.AutoField(primary_key=True)
    swo_id = models.ForeignKey(Social_welfare_officers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationSWO(models.Model):
    id = models.AutoField(primary_key=True)
    swo_id = models.ForeignKey(Social_welfare_officers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationSWO(models.Model):
    id = models.AutoField(primary_key=True)
    swo_id = models.ForeignKey(Social_welfare_officers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackCEO(models.Model):
    id = models.AutoField(primary_key=True)
    ceo_id = models.ForeignKey(CEO, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationCEO(models.Model):
    id = models.AutoField(primary_key=True)
    ceo_id = models.ForeignKey(CEO, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationCEO(models.Model):
    id = models.AutoField(primary_key=True)
    ceo_id = models.ForeignKey(CEO, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationCEO(models.Model):
    id = models.AutoField(primary_key=True)
    ceo_id = models.ForeignKey(CEO, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackCS(models.Model):
    id = models.AutoField(primary_key=True)
    cs_id = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CSFeedBackHR(models.Model):
    id = models.AutoField(primary_key=True)
    cs_id = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationCS(models.Model):
    id = models.AutoField(primary_key=True)
    cs_id = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationCS(models.Model):
    id = models.AutoField(primary_key=True)
    cs_id = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationCS(models.Model):
    id = models.AutoField(primary_key=True)
    cs_id = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackH_Admin(models.Model):
    id = models.AutoField(primary_key=True)
    h_admin_id = models.ForeignKey(H_AdminHOD, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationH_Admin(models.Model):
    id = models.AutoField(primary_key=True)
    h_admin_id = models.ForeignKey(H_AdminHOD, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationH_Admin(models.Model):
    id = models.AutoField(primary_key=True)
    h_admin_id = models.ForeignKey(H_AdminHOD, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationH_Admin(models.Model):
    id = models.AutoField(primary_key=True)
    h_admin_id = models.ForeignKey(H_AdminHOD, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationDriver(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Drivers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationDriver(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Drivers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DefendantNotificationAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccusserNotificationAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Goals(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Code_of_Conduct(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponsibilityHR(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponsibilityCEO(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponsibilityLawyers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponsibilityCS(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponsibilitySWO(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponsibilityAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponsibilityAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalaryHR(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalaryAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalarySWO(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalaryLawyer(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalaryAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalaryCS(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalaryCEO(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Overdue(models.Model):
    id = models.AutoField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    name = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE)
    amount = models.FloatField()
    year = models.FloatField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportCEO(models.Model):
    id = models.AutoField(primary_key=True)
    ceo_id = models.ForeignKey(CEO, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportSWO(models.Model):
    id = models.AutoField(primary_key=True)
    swo_id = models.ForeignKey(Social_welfare_officers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportCS(models.Model):
    id = models.AutoField(primary_key=True)
    cs_id = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportH_Admin(models.Model):
    id = models.AutoField(primary_key=True)
    h_admin_id = models.ForeignKey(H_AdminHOD, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportLawyer(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer_id = models.ForeignKey(Lawyers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportCEO(models.Model):
    id = models.AutoField(primary_key=True)
    ceo_id = models.ForeignKey(CEO, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportHR(models.Model):
    id = models.AutoField(primary_key=True)
    hr_id = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportSWO(models.Model):
    id = models.AutoField(primary_key=True)
    swo_id = models.ForeignKey(Social_welfare_officers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportAccountant(models.Model):
    id = models.AutoField(primary_key=True)
    accountant_id = models.ForeignKey(Accountant, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportCS(models.Model):
    id = models.AutoField(primary_key=True)
    cs_id = models.ForeignKey(Customer_service, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportH_Admin(models.Model):
    id = models.AutoField(primary_key=True)
    h_admin_id = models.ForeignKey(H_AdminHOD, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin_id = models.ForeignKey(AdminHOD, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PermissionReportLawyer(models.Model):
    id = models.AutoField(primary_key=True)
    lawyer_id = models.ForeignKey(Lawyers, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SWMeeting(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Apartment_owners, on_delete=models.CASCADE)
    tenant_id = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    apartment_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    applied_person = models.CharField(max_length=20)
    reason = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    decision = models.CharField(max_length=70)
    dec_reason = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CEOMeeting(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_name = models.CharField(max_length=255)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HRMeeting(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_name = models.CharField(max_length=255)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CEOTopics(models.Model):
    id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=255)
    meeting_id = models.ForeignKey(CEOMeeting, on_delete=models.CASCADE, default=1)  # need to give default course
    ceo_id = models.ForeignKey(CEO, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HRTopics(models.Model):
    id = models.AutoField(primary_key=True)
    topic_name = models.CharField(max_length=255)
    meeting_id = models.ForeignKey(HRMeeting, on_delete=models.CASCADE, default=1)  # need to give default course
    hr_id = models.ForeignKey(Human_resource_managers, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceHRReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    attendant_id = models.ForeignKey(S_CustomUser, on_delete=models.DO_NOTHING, related_name= "or_hr_atr")
    meeting_id = models.ForeignKey(HRMeeting, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceCEOReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    attendant_id = models.ForeignKey(S_CustomUser, on_delete=models.DO_NOTHING, related_name= "or_ceo_atr")
    meeting_id = models.ForeignKey(CEOMeeting, on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DiscplineMeeting(models.Model):
    id = models.AutoField(primary_key=True)
    defendant_name = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE, related_name="def_name")
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    accuser_name = models.ForeignKey(S_CustomUser, on_delete=models.CASCADE,  related_name="acc_name")
    date = models.DateTimeField()
    accusation = models.TextField()
    verdict = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApartmentPayment(models.Model):
    id = models.AutoField(primary_key=True)
    receipt_number = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=30)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    payed_object = models.ForeignKey(Album, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Incomes(models.Model):
    id = models.AutoField(primary_key=True)
    receipt_number = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=30)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    amount = models.FloatField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBack(models.Model):
    id = models.AutoField(primary_key=True)
    communication = models.CharField(max_length=100)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    replied_by = models.ForeignKey(Customer_service, on_delete=models.CASCADE, null=True, blank=True)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

