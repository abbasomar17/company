from django.contrib import admin

from .models import *
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass


myModels = [S_CustomUser, FeedBack, Office, Rate, CEO, Human_resource_managers, Lawyers, Customer_service, Accountant, ResponsibilityCEO, Social_welfare_officers, Discpline_committee, FeedBackHR, NotificationHR, DefendantNotificationHR, AccuserNotificationHR, FeedBackLawyer, NotificationLawyer, DefendantNotificationLawyer, AccusserNotificationLawyer, FeedBackAccountant, NotificationAccountant, DefendantNotificationAccountant, AccusserNotificationAccountant, FeedBackSWO, NotificationSWO, DefendantNotificationSWO, AccusserNotificationSWO, FeedBackCEO, NotificationCEO, DefendantNotificationCEO, AccusserNotificationCEO, FeedBackCS, NotificationCS, DefendantNotificationCS, AccusserNotificationCS, FeedBackAdmin, DefendantNotificationAdmin, AccusserNotificationAdmin, NotificationAdmin, FeedBackH_Admin, DefendantNotificationH_Admin, AccusserNotificationH_Admin, NotificationH_Admin, DefendantNotificationDriver, AccusserNotificationDriver, Goals, Code_of_Conduct, ResponsibilitySWO, ResponsibilityHR, ResponsibilityCS, ResponsibilityAdmin, ResponsibilityAccountant, ResponsibilityLawyers, SalarySWO, SalaryHR, SalaryCS, SalaryLawyer, SalaryAccountant, SalaryAdmin, SalaryCEO, Overdue, LeaveReportLawyer, LeaveReportAccountant, LeaveReportCS, LeaveReportHR, LeaveReportAdmin, LeaveReportCEO, LeaveReportH_Admin, LeaveReportSWO, PermissionReportCS, PermissionReportHR, PermissionReportAdmin, PermissionReportH_Admin, PermissionReportLawyer, PermissionReportAccountant, PermissionReportCEO, PermissionReportSWO, SWMeeting, CEOMeeting, HRMeeting, HRTopics, CEOTopics, AttendanceCEOReport,  AttendanceHRReport, DiscplineMeeting, ApartmentPayment, Incomes]
admin.site.register(myModels, AuthorAdmin)
