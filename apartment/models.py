from django.contrib.auth.models import AbstractUser, AbstractBaseUser, User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
import uuid
from django.shortcuts import reverse
from django.db import models


class ApartmentBooking(models.Model):
    booking_date = models.DateTimeField(auto_now_add=True)
    meeting_date = models.DateTimeField()
    booking_id = models.CharField(max_length=30)

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):


#     return self.course_name

# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now=True)
    user_type_data = ((1, "HOD"), (2, "Apartment_owners"), (3, "Tenants"), (4, "Drivers"),(5, "Random_users"),)
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)  # need to give default course
    owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Apartment_owners(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Drivers(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    region = models.CharField(max_length=30)
    current_address = models.TextField(null=True, blank=True)
    familiar_address = models.TextField(null=True, blank=True)
    working_address = models.TextField(null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    vehicle_type = models.CharField(max_length=30, null=True, blank=True)
    nida_number = models.CharField(max_length=30)
    tin_number = models.CharField(max_length=20)
    lnumber = models.CharField(max_length=30)
    pnumber = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=20)
    profile_picture = models.FileField(upload_to='profile_picture')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nida_number

class Vehicles(models.Model):
    id = models.AutoField(primary_key=True)
    current_address = models.TextField()
    familiar_address = models.TextField()
    working_address = models.TextField()
    driver_id = models.ForeignKey(Drivers, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=30)
    pnumber = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pnumber


class Random_users(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportOwner(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Apartment_owners, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackOwner(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Apartment_owners, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackDriver(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Drivers, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=70)
    spec_location = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    town = models.CharField(max_length=20)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    discount_price = models.FloatField(blank=True, null=True)
    real_price = models.FloatField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    labels = models.CharField(max_length=20)
    booking_id = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField()
    thumb = models.ImageField(upload_to='albums')
    owner_id = models.ForeignKey(Apartment_owners, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)

    #def get_absolute_url(self):
    #    return reverse('album', kwargs={'slug':self.slug})

    def __unicode__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('album', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'slug': self.slug
        })

    def get_real_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    def save(self, *args, **kwargs):
        """Override the save method to set the order number."""
        if not self.real_price:
            self.real_price = self.get_real_price()
        super().save(*args, **kwargs)


class AlbumImage(models.Model):
    image = models.ImageField(upload_to='albums')
    thumb = models.ImageField(upload_to='albums')
    album = models.ForeignKey('album', on_delete=models.PROTECT)
    alt = models.CharField(max_length=255, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=70, default=uuid.uuid4, editable=False)


class Tenants(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    nida_number = models.CharField(max_length=30)
    owner_id = models.ForeignKey(Apartment_owners, on_delete=models.CASCADE)
    apartment_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nida_number


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey(Tenants, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackTenant(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportTenant(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    Country = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=50)
    amounts = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "order_user")
    ref_code = models.CharField(
        max_length=32, null=False, editable=False
    )
    phone = models.CharField(max_length=25)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    total_paid = models.FloatField()
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    being_received = models.BooleanField(default=False)
    refund_request = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ref_code)

    def _generate_ref_code(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def get_total(self):
        total = 0
        items = self.get_order_items()
        for order_item in items.all():
            total += order_item.get_final_price()
        if self.coupon is not None:
            total -= self.coupon.amount
        return total

    def save(self, *args, **kwargs):
        """Override the save method to set the order number."""
        if not self.ref_code:
            self.ref_code = self._generate_ref_code()
        super().save(*args, **kwargs)
        if not self.total_paid:
            self.total_paid = self.get_total()
        super().save(*args, **kwargs)

    def get_order_items(self):
        """Get the order items for the order."""
        items = OrderApartment.objects.filter(order=self)
        return items


class OrderApartment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_ap_user")
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_item'
    )
    item = models.ForeignKey(Album, on_delete=models.CASCADE)
    saved_amount = models.FloatField()
    final_price = models.FloatField()
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_add_single_item_to_cart_url(self):
        return reverse('add-item-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_single_item_from_cart_url(self):
        return reverse('remove_item_from_cart', kwargs={
            'slug': self.slug
        })

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        if self.item.discount_price:
            return self.get_total_item_price() - self.get_total_discount_item_price()
        return 0

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def save(self, *args, **kwargs):
        """Override the save method to set the order number."""
        if not self.final_price:
            self.final_price = self.get_final_price()
        super().save(*args, **kwargs)
        if not self.saved_amount:
            self.saved_amount = self.get_amount_saved()
        super().save(*args, **kwargs)


class NotificationTenant(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationOwner(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Apartment_owners, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationDriver(models.Model):
    id = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Drivers, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationRandom(models.Model):
    """Model for stock email notifications."""
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Random_users,
        on_delete=models.CASCADE,
        verbose_name='Requested user',
        help_text='Requested user.'
    )
    requested_product = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        verbose_name='Requested product',
        help_text='Requested product.',
        related_name='email_product'
    )
    requested_quantity = models.PositiveIntegerField(
        verbose_name='Requested quantity',
        help_text='Requested quantity.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )
    answer_sent = models.BooleanField(
        default=False,
        verbose_name='Answer send',
        help_text='Answer send.'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.admin.user.username

    def get_all_not_sent(self):
        """Return all not send back to stock email notifications."""
        return NotificationRandom.objects.filter(answer_sent=False)

    def save(self, *args, **kwargs):
        super().save()
        subject, from_email, to = (
            'Booking email notification', 'abbasoa17@gmail.com', [self.user.admin.user.email]
        )
        text_content = ''
        html_content = (
            '<h1 style="color:indigo; text-align:center">'
            'Booking email notification</h1><br><strong>Your request has '
            'been sent to the administrator.</strong><br><p><strong>Apartment: '
            '</strong>' + self.requested_product.title + '</p><p><strong>'
            'Months: </strong>' + str(self.requested_quantity) + '</p>'
            '<br><br><strong>Visit our office at 8:00 AM at any day from' + str(self.requested_product.session_year_id.session_start_year) + 'to' + str(self.requested_product.session_year_id.session_end_year) +'! </strong><br><br>'
            '<a href="https://abbas.onrender.com">'
            'Go to Website</a><br><br>'
            '<p>Thank you for being with us!</p>'
            '<em>Online Apartment Booking</em>'
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        self.answer_sent = True
        super().save(*args, **kwargs)


class RequestTermination(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.ForeignKey(Apartment_owners, on_delete=models.CASCADE)
    tenant_id = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    apartment_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    applied_person = models.CharField(max_length=20)
    reason = models.TextField()
    accepted = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ApartmentResult(models.Model):
    id = models.AutoField(primary_key=True)
    tenant_id = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    apartment_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    apartment_exam_marks = models.IntegerField(default=0)
    apartment_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmailRandomsNotification(models.Model):
    """Model for email news notifications."""
    id = models.AutoField(primary_key=True)
    email_name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email name',
        help_text='Email name.'
    )
    content = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name='Content',
        help_text='Content.'
    )
    code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Code',
        help_text='Code.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )

    class Meta:
        """Meta class for email news notifications."""
        verbose_name = 'Email randoms notification'
        verbose_name_plural = 'Email randoms notifications'

    def __str__(self):
        """Return the name of the email news notification."""
        return self.email_name

    def save(self, *args, **kwargs):
        super().save()
        users = Random_users.objects.all()
        recipients = [user.admin.user.email for user in users]
        subject, from_email, to = (
            self.email_name, 'abbasoa17@gmail.com', recipients
        )
        text_content = ''
        if self.code is not None:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p style="text-align:center; font-style: italic;">'
                'Only for our loyal customers!</p><br>'
                '<p>' + self.content + '</p><br>'
                '<p style="text-align:center"><em>Use the code below for the purpose explained '
                'in this email</em></p>'
                '<br><br><p style="color:SlateBlue;'
                'background-color:Lavender; padding:1em 2em;'
                'text-align:center; font-weight:bold">' +
                self.code + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        else:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p>' + self.content + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


class EmailTenantsNotification(models.Model):
    """Model for email news notifications."""
    id = models.AutoField(primary_key=True)
    email_name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email name',
        help_text='Email name.'
    )
    content = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name='Content',
        help_text='Content.'
    )
    code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Code',
        help_text='Code.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )

    class Meta:
        """Meta class for email news notifications."""
        verbose_name = 'Email tenants notification'
        verbose_name_plural = 'Email tenants notifications'

    def __str__(self):
        """Return the name of the email news notification."""
        return self.email_name

    def save(self, *args, **kwargs):
        super().save()
        users = Tenants.objects.all()
        recipients = [user.admin.user.email for user in users]
        subject, from_email, to = (
            self.email_name, 'abbasoa17@gmail.com', recipients
        )
        text_content = ''
        if self.code is not None:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p style="text-align:center; font-style: italic;">'
                'Only for our loyal customers!</p><br>'
                '<p>' + self.content + '</p><br>'
                '<p style="text-align:center"><em>Use the code below for the purpose explained '
                'in this email</em></p>'
                '<br><br><p style="color:SlateBlue;'
                'background-color:Lavender; padding:1em 2em;'
                'text-align:center; font-weight:bold">' +
                self.code + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        else:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p>' + self.content + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


class EmailOwnersNotification(models.Model):
    """Model for email news notifications."""
    id = models.AutoField(primary_key=True)
    email_name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email name',
        help_text='Email name.'
    )
    content = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name='Content',
        help_text='Content.'
    )
    code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Code',
        help_text='Code.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )

    class Meta:
        """Meta class for email news notifications."""
        verbose_name = 'Email onwers notification'
        verbose_name_plural = 'Email owners notifications'

    def __str__(self):
        """Return the name of the email news notification."""
        return self.email_name

    def save(self, *args, **kwargs):
        super().save()
        users = Apartment_owners.objects.all()
        recipients = [user.admin.user.email for user in users]
        subject, from_email, to = (
            self.email_name, 'abbasoa17@gmail.com', recipients
        )
        text_content = ''
        if self.code is not None:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p style="text-align:center; font-style: italic;">'
                'Only for our loyal customers!</p><br>'
                '<p>' + self.content + '</p><br>'
                '<p style="text-align:center"><em>Use the code below for the purpose explained '
                'in this email</em></p>'
                '<br><br><p style="color:SlateBlue;'
                'background-color:Lavender; padding:1em 2em;'
                'text-align:center; font-weight:bold">' +
                self.code + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        else:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p>' + self.content + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


class EmailDriversNotification(models.Model):
    """Model for email news notifications."""
    id = models.AutoField(primary_key=True)
    email_name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email name',
        help_text='Email name.'
    )
    content = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name='Content',
        help_text='Content.'
    )
    code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Code',
        help_text='Code.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )

    class Meta:
        """Meta class for email news notifications."""
        verbose_name = 'Email drivers notification'
        verbose_name_plural = 'Email drivers notifications'

    def __str__(self):
        """Return the name of the email news notification."""
        return self.email_name

    def save(self, *args, **kwargs):
        super().save()
        users = Drivers.objects.all()
        recipients = [user.admin.user.email for user in users]
        subject, from_email, to = (
            self.email_name, 'abbasoa17@gmail.com', recipients
        )
        text_content = ''
        if self.code is not None:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p style="text-align:center; font-style: italic;">'
                'Only for our loyal customers!</p><br>'
                '<p>' + self.content + '</p><br>'
                '<p style="text-align:center"><em>Use the code below for the purpose explained '
                'in this email</em></p>'
                '<br><br><p style="color:SlateBlue;'
                'background-color:Lavender; padding:1em 2em;'
                'text-align:center; font-weight:bold">' +
                self.code + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        else:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p>' + self.content + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


class EmailAdminsNotification(models.Model):
    """Model for email news notifications."""
    id = models.AutoField(primary_key=True)
    email_name = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email name',
        help_text='Email name.'
    )
    content = models.TextField(
        max_length=1500,
        null=False,
        blank=False,
        verbose_name='Content',
        help_text='Content.'
    )
    code = models.CharField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Code',
        help_text='Code.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at',
    )

    class Meta:
        """Meta class for email news notifications."""
        verbose_name = 'Email admins notification'
        verbose_name_plural = 'Email admins notifications'

    def __str__(self):
        """Return the name of the email news notification."""
        return self.email_name

    def save(self, *args, **kwargs):
        super().save()
        users = AdminHOD.objects.all()
        recipients = [user.admin.user.email for user in users]
        subject, from_email, to = (
            self.email_name, 'abbasoa17@gmail.com', recipients
        )
        text_content = ''
        if self.code is not None:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p style="text-align:center; font-style: italic;">'
                'Only for our loyal customers!</p><br>'
                '<p>' + self.content + '</p><br>'
                '<p style="text-align:center"><em>Use the code below for the purpose explained '
                'in this email</em></p>'
                '<br><br><p style="color:SlateBlue;'
                'background-color:Lavender; padding:1em 2em;'
                'text-align:center; font-weight:bold">' +
                self.code + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        else:
            html_content = (
                '<h1 style="color:indigo; text-align:center">' +
                self.email_name +
                '</h1><br><p>' + self.content + '</p>'
                '<br><br><strong>Feel free to visit our offices! </strong><br><br>'
                '<p>Thank you for being with us!</p>'
                '<em>Online Residence Booking</em>'
            )
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        