#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from django import forms
from django.forms import Form
from django.contrib.auth.models import User
from .models import *

class DateInput(forms.DateInput):
    input_type = "date"

class OrderForm(forms.ModelForm):
    """Form for Order Model"""
    class Meta:
        model = Order
        fields = [
            'phone',
            'ordered_date',
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'ordered_date': forms.DateInput(attrs={'class': 'form-control'}),
        }


class OrderItemForm(forms.ModelForm):
    """Form for OrderItem Model"""
    class Meta:
        model = OrderApartment
        fields = [
            'order',
            'item',
            'quantity',
        ]
        widgets = {
            'order': forms.HiddenInput(),
            'item': forms.HiddenInput(),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddTenantForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    try:
        apartments = Album.objects.all()
        apartment_list = []
        for apartment in apartments:
            single_apartment = (apartment.id, apartment.title)
            apartment_list.append(single_apartment)
    except:
        apartment_list = []

    try:
        owners = Apartment_owners.objects.all()
        owner_list = []
        for owner in owners:
            single_owner = (owner.id, owner.admin.user.first_name + " " +  owner.admin.user.last_name)
            owner_list.append(single_owner)
    except:
        owner_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
            session_year.id, str(session_year.session_start_year) + " to " + str(session_year.session_end_year))
            session_year_list.append(single_session_year)
    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    owner_id = forms.ChoiceField(label="Apartment Owner", choices=owner_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    apartment_id = forms.ChoiceField(label="Apartment Name", choices=apartment_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    course_id = forms.ChoiceField(label="Meeting Attended", choices=course_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class EditTenantForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    # For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    # For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
            session_year.id, str(session_year.session_start_year) + " to " + str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    course_id = forms.ChoiceField(label="Course", choices=course_list,
                                  widget=forms.Select(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class AddDriverForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    region = forms.CharField(label="Region", max_length=30,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    current_address = forms.CharField(label="Current Address", required=False, max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    familiar_address = forms.CharField(label="Familiar Address", required=False, max_length=50,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    working_address = forms.CharField(label="Working Address", required=False, max_length=50,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    nida_number = forms.CharField(label="Nida Number", max_length=30,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    tin_number = forms.CharField(label="Tin Number", max_length=20,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    lnumber = forms.CharField(label="License Number", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    pnumber = forms.CharField(label="Plate Number", max_length=30, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile_number = forms.CharField(label="Mobile Number", required=False, max_length=20,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    vehicle_list = (
        ('Motorcycle', 'Motorcycle'),
        ('Guta', 'Guta'),
        ('Bajaji', 'Bajaji'),
        ('Car', 'Car')
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    vehicle_type = forms.ChoiceField(label="Vehicle Type", choices=vehicle_list, required=False,
                               widget=forms.Select(attrs={"class": "form-control"}))
    profile_picture = forms.FileField(label="Profile Picture", required=False,
                                      widget=forms.FileInput(attrs={"class": "form-control"}))


class EditDriverForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    current_address = forms.CharField(label="Current Address", required=False,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    familiar_address = forms.CharField(label="Familiar Address", required=False,
                                       widget=forms.TextInput(attrs={"class": "form-control"}))
    working_address = forms.CharField(label="Working Address", required=False,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    vehicle_list = (
        ('Motorcycle', 'Motorcycle'),
        ('Guta', 'Guta'),
        ('Bajaji', 'Bajaji'),
        ('Car', 'Car')
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    vehicle_type = forms.ChoiceField(label="Vehicle Type", choices=vehicle_list, required=False,
                                     widget=forms.Select(attrs={"class": "form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_picture = forms.FileField(label="Profile Picture", required=False,
                                      widget=forms.FileInput(attrs={"class": "form-control"}))


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name']


class AddOwnerForm(forms.ModelForm):
    class Meta:
        model = Apartment_owners
        fields = ['address']


class AlbumForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    spec_location = forms.CharField(label="Specific Location", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    region = forms.CharField(label="Region", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    town = forms.CharField(label="Town", max_length=50,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.FloatField(label="Price", required=True,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))
    discount_price = forms.CharField(label="Discount Price", required=False,
                                      widget=forms.NumberInput(attrs={"class": "form-control"}))
    quantity = forms.FloatField(label="Quantity", required=True,
                             widget=forms.NumberInput(attrs={"class": "form-control"}))
    booking_id = forms.CharField(label="Booking Id", max_length=30, required=False,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))

    CATEGORY_CHOICES = (
        ('Normal Room', 'Normal Room'),
        ('Self Room', 'Self Room'),
        ('Room with living Room', 'Room with living Room'),
        ('Full House', 'Full House'),
        ('Guest House', 'Guest House'),
        ('Lounge', 'Lounge'),
        ('Hotel', 'Hotel'),
    )

    LABEL_CHOICES = (
        ('For Sale', 'For sale'),
        ('For Rent', 'For Rent'),
        ('Not available now', 'Not available now'),
    )

    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
            session_year.id, str(session_year.session_start_year) + " to " + str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    try:
        owners = Apartment_owners.objects.all()
        owner_list = []
        for owner in owners:
            single_owner = (
            owner.id, str(owner.admin.user.first_name) + " " + str(owner.admin.user.last_name))
            owner_list.append(single_owner)

    except:
        owner_list = []

    category = forms.ChoiceField(label="Category", choices=CATEGORY_CHOICES,
                               widget=forms.Select(attrs={"class": "form-control"}))
    labels = forms.ChoiceField(label="Labels", choices=LABEL_CHOICES,
                                     widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    owner_id = forms.ChoiceField(label="Apartment Owner", choices=owner_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    thumb = forms.FileField(label="Thumb", required=True,
                                      widget=forms.FileInput(attrs={"class": "form-control"}))
    zip = forms.FileField(required=False)

class EditApartmentForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50,
                            widget=forms.TextInput(attrs={"class": "form-control"}))
    spec_location = forms.CharField(label="Specific Location", max_length=50,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    region = forms.CharField(label="Region", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    town = forms.CharField(label="Town", max_length=50,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    price = forms.FloatField(label="Price", required=True,
                             widget=forms.NumberInput(attrs={"class": "form-control"}))
    discount_price = forms.CharField(label="Discount Price", required=False,
                                     widget=forms.NumberInput(attrs={"class": "form-control"}))
    quantity = forms.FloatField(label="Quantity", required=True,
                             widget=forms.NumberInput(attrs={"class": "form-control"}))
    booking_id = forms.CharField(label="Booking Id", max_length=30, required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))

    CATEGORY_CHOICES = (
        ('Normal Room', 'Normal Room'),
        ('Self Room', 'Self Room'),
        ('Room with living Room', 'Room with living Room'),
        ('Full House', 'Full House'),
        ('Guest House', 'Guest House'),
        ('Lodge', 'Lodge'),
        ('Hotel', 'Hotel'),
    )

    LABEL_CHOICES = (
        ('For Sale', 'For sale'),
        ('For Rent', 'For Rent'),
        ('Not available now', 'Not available now'),
    )

    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (
            session_year.id, str(session_year.session_start_year) + " to " + str(session_year.session_end_year))
            session_year_list.append(single_session_year)

    except:
        session_year_list = []

    try:
        owners = Apartment_owners.objects.all()
        owner_list = []
        for owner in owners:
            single_owner = (
            owner.id, str(owner.admin.user.first_name) + " " + str(owner.admin.user.last_name))
            owner_list.append(single_owner)

    except:
        owner_list = []


    category = forms.ChoiceField(label="Gender", choices=CATEGORY_CHOICES,
                                 widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    owner_id = forms.ChoiceField(label="Apartment Owner", choices=owner_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    labels = forms.ChoiceField(label="Vehicle Type", choices=LABEL_CHOICES,
                               widget=forms.Select(attrs={"class": "form-control"}))
    thumb = forms.FileField(label="Best View Picture", required=False,
                            widget=forms.FileInput(attrs={"class": "form-control"}))


class AddVehicleForm(forms.Form):
    pnumber = forms.CharField(label="Vehicle Plate Number", max_length=30, required=True,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile_number = forms.CharField(label="Mobile Number", max_length=20, required=True,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    current_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))

    familiar_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5
    }))

    working_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 6
    }))

    vehicle_list = (
        ('Motorcycle', 'Motorcycle'),
        ('Guta', 'Guta'),
        ('Bajaji', 'Bajaji'),
        ('Car', 'Car')
    )


    try:
        drivers = Drivers.objects.all()
        driver_list = []
        for driver in drivers:
            single_driver = (
            driver.id, str(driver.admin.user.first_name) + " " + str(driver.admin.user.last_name))
            driver_list.append(single_driver)

    except:
        driver_list = []

    vehicle_type = forms.ChoiceField(label="Vehicle Type", choices=vehicle_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    driver_id = forms.ChoiceField(label="Driver", choices=driver_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))

class DriverAddVehicleForm(forms.Form):
    pnumber = forms.CharField(label="Vehicle Plate Number", max_length=30, required=True,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile_number = forms.CharField(label="Mobile Number", max_length=20, required=True,
                                    widget=forms.TextInput(attrs={"class": "form-control"}))
    current_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))

    familiar_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5
    }))

    working_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 6
    }))

    vehicle_list = (
        ('Motorcycle', 'Motorcycle'),
        ('Guta', 'Guta'),
        ('Bajaji', 'Bajaji'),
        ('Car', 'Car')
    )

    vehicle_type = forms.ChoiceField(label="Vehicle Type", choices=vehicle_list,
                                     widget=forms.Select(attrs={"class": "form-control"}))


class EditVehicleForm(forms.Form):
    pnumber = forms.CharField(label="Vehicle Plate Number", max_length=30, required=True,
                                      widget=forms.TextInput(attrs={"class": "form-control"}))
    mobile_number = forms.CharField(label="Mobile Number", max_length=20, required=True,
                                  widget=forms.TextInput(attrs={"class": "form-control"}))
    current_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))

    familiar_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5
    }))

    working_address = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 6
    }))

    vehicle_list = (
        ('Motorcycle', 'Motorcycle'),
        ('Guta', 'Guta'),
        ('Bajaji', 'Bajaji'),
        ('Car', 'Car')
    )


    try:
        drivers = Drivers.objects.all()
        driver_list = []
        for driver in drivers:
            single_driver = (
            driver.id, str(driver.admin.user.first_name) + " " + str(driver.admin.user.last_name))
            driver_list.append(single_driver)

    except:
        driver_list = []

    vehicle_type = forms.ChoiceField(label="Vehicle Type", choices=vehicle_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    driver_id = forms.ChoiceField(label="Driver", choices=driver_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))


class CheckForm(forms.Form):
    PAYMENT_CHOICES = (
        ('stripe', 'stripe'),
        ('paypal', 'paypal')
    )
    street_address = forms.CharField(label="Street Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    apartment_address = forms.CharField(label="Apartment Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    country = forms.CharField(label="Country", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    zip = forms.CharField(label="zip", max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(label="code", max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))

class RefundForm(forms.Form):
    ref_code = forms.CharField(label="ref_code", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))


class EmailOwnersNotificationForm(forms.ModelForm):
    """Form for email news notifications."""
    class Meta:
        """Meta class for email news notifications."""
        model = EmailOwnersNotification
        fields = ['email_name', 'content', 'code']

        widgets = {
            'email_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add email name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add email content',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add code if needed',
            }),
        }


class EmailTenantsNotificationForm(forms.ModelForm):
    """Form for email news notifications."""
    class Meta:
        """Meta class for email news notifications."""
        model = EmailTenantsNotification
        fields = ['email_name', 'content', 'code']

        widgets = {
            'email_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add email name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add email content',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add code if needed',
            }),
        }


class EmailDriversNotificationForm(forms.ModelForm):
    """Form for email news notifications."""
    class Meta:
        """Meta class for email news notifications."""
        model = EmailDriversNotification
        fields = ['email_name', 'content', 'code']

        widgets = {
            'email_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add email name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add email content',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add code if needed',
            }),
        }


class EmailRandomsNotificationForm(forms.ModelForm):
    """Form for email news notifications."""
    class Meta:
        """Meta class for email news notifications."""
        model = EmailRandomsNotification
        fields = ['email_name', 'content', 'code']

        widgets = {
            'email_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add email name',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add email content',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add code if needed',
            }),
        }
