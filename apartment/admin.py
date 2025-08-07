from django.contrib import admin


from .models import CustomUser, SessionYearModel, NotificationRandom, EmailRandomsNotification, EmailOwnersNotification, EmailTenantsNotification, EmailDriversNotification, EmailAdminsNotification, Random_users, Drivers, AlbumImage, Album, RequestTermination, Order, OrderApartment, Coupon, BillingAddress, Payment, FeedBackDriver, Apartment_owners, Courses, Subjects, Tenants, Attendance, AttendanceReport, LeaveReportTenant, LeaveReportOwner, FeedBackTenant, FeedBackOwner, NotificationTenant, NotificationOwner, NotificationDriver, ApartmentResult

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_request=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to granted'

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'ordered',
        'being_delivered',
        'being_received',
        'refund_request',
        'refund_granted',
        'billing_address',
        'payment',
        'coupon',
    ]
    list_display_links = [
        'user',
        'billing_address',
        'payment',
        'coupon',
    ]
    list_filter = [
        'being_delivered',
        'being_received',
        'refund_request',
        'refund_granted',
    ]
    search_fields = [
        'user__username',
        'ref_code',
    ]
    actions = [make_refund_accepted]


admin.site.register(Order, OrderAdmin)


class AuthorAdmin(admin.ModelAdmin):
    pass
myModels = [ CustomUser, SessionYearModel,NotificationRandom, EmailRandomsNotification, EmailOwnersNotification, EmailTenantsNotification, EmailDriversNotification, EmailAdminsNotification, Drivers, Random_users, AlbumImage, Album, RequestTermination, FeedBackDriver, Apartment_owners, Courses, Subjects, Tenants, Attendance, AttendanceReport, LeaveReportTenant, LeaveReportOwner, FeedBackTenant, FeedBackOwner, NotificationTenant, NotificationOwner, NotificationDriver, ApartmentResult, OrderApartment, Coupon, BillingAddress, Payment]
admin.site.register(myModels, AuthorAdmin)
